#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ----------------- CONFIGURATION VARIABLES -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/inventory_data")
OUT_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

IGNORE_PRE = "/nluu6p/home/"
# -----------------------------------------------------------

# Step 1: FIND CSV FILES
csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))
print(f"Found {len(csv_files)} CSV files:")
for f in csv_files:
    print(f" - {f}")

# Step 2: READ CSVs AND FIX HEADER
df_list = []
columns_sets = []

for f in csv_files:
    with open(f, "r") as fh:
        header_line = fh.readline().strip()
        fixed_header = header_line.replace("COLL_NAME,DATA_NAME", "COLL_NAME/DATA_NAME").split(",")

    df = pd.read_csv(f, header=0, names=fixed_header, skiprows=1)
    df["source_dir"] = f.parent.name
    df_list.append(df)
    columns_sets.append(set(df.columns))

# Step 3: CHECK CONSISTENCY
first_columns = columns_sets[0]
for i, cols in enumerate(columns_sets):
    if cols != first_columns:
        print(f"Inconsistent columns in: {csv_files[i]}")
        exit()

print("All inventory CSVs consistent.")

# Step 4: COMBINE
full_df = pd.concat(df_list, ignore_index=True)
full_df.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)

# Ensure numeric
full_df["DATA_SIZE"] = pd.to_numeric(full_df["DATA_SIZE"], errors="coerce").fillna(0)

print(f"Total rows imported: {len(full_df)}")

# Step 5: NORMALIZE PATHS
full_df["rel_path"] = full_df["COLL_NAME"].apply(lambda x: str(x).replace(IGNORE_PRE, "", 1))
full_df["file_name"] = full_df["rel_path"].apply(lambda x: Path(x).name)

# Step 6: KEEP ONLY FILES
full_df["is_file"] = full_df["file_name"].apply(lambda x: "." in x)
file_df = full_df[full_df["is_file"]].copy()

# Step 7: REMOVE TRIVIAL FILES
trivial_files = [".DS_Store", "Thumbs.db", "Desktop.ini"]
file_df = file_df[~file_df["file_name"].isin(trivial_files)].copy()

print(f"Total file-level rows: {len(file_df)}")

# ---------------- DUPLICATE DETECTION ----------------

# Ensure checksum is string (important!)
file_df["DATA_CHECKSUM"] = file_df["DATA_CHECKSUM"].astype(str)

# Flag duplicates
file_df["dup_checksum"] = (
    file_df["DATA_CHECKSUM"].notna() &
    (file_df["DATA_CHECKSUM"] != "") &
    file_df.duplicated("DATA_CHECKSUM", keep=False)
)

file_df["dup_name"] = file_df.duplicated("file_name", keep=False)

file_df["dup_both"] = file_df["dup_checksum"] & file_df["dup_name"]

# ---------------- FINAL OUTPUT ----------------

output_df = file_df[[
    "file_name",
    "DATA_CHECKSUM",
    "dup_checksum",
    "dup_name",
    "dup_both"
]].copy()

# Rename for clarity
output_df.rename(columns={
    "DATA_CHECKSUM": "checksum"
}, inplace=True)

# Optional: sort for readability
output_df = output_df.sort_values(
    by=["dup_both", "dup_checksum", "dup_name"],
    ascending=False
)

# Step 8: SAVE
OUT_DIR.mkdir(parents=True, exist_ok=True)
out_file = OUT_DIR / "duplicate_detection.csv"

output_df.to_csv(out_file, index=False)

print(f"Saved structured duplicate file to: {out_file}")
print(f"Total rows in output: {len(output_df)}")