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

    df = pd.read_csv(f, header=0, names=fixed_header, skiprows=1, dtype=str)
    df["source_dir"] = f.parent.name
    df_list.append(df)
    columns_sets.append(set(df.columns))

# Step 3: CHECK COLUMN CONSISTENCY
first_columns = columns_sets[0]
for i, cols in enumerate(columns_sets):
    if cols != first_columns:
        print(f"Inconsistent columns in: {csv_files[i]}")
        exit()

print("All inventory CSVs consistent.")

# Step 4: COMBINE CSVs
full_df = pd.concat(df_list, ignore_index=True)
full_df.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)

# Ensure numeric DATA_SIZE
full_df["DATA_SIZE"] = pd.to_numeric(full_df.get("DATA_SIZE", 0), errors="coerce").fillna(0).astype(int)
print(f"Total rows imported: {len(full_df)}")

# Step 5: NORMALIZE PATHS
full_df["rel_path"] = full_df["COLL_NAME"].apply(lambda x: str(x).replace(IGNORE_PRE, "", 1))

# Step 6: KEEP ONLY FILES
full_df["is_file"] = full_df["rel_path"].apply(lambda x: "." in Path(x).name)
file_df = full_df[full_df["is_file"]].copy()

# Step 7: REMOVE TRIVIAL FILES
trivial_files = [".DS_Store", "Thumbs.db", "Desktop.ini"]
file_df = file_df[~file_df["rel_path"].apply(lambda x: Path(x).name in trivial_files)].copy()
print(f"Total file-level rows after cleaning trivial files: {len(file_df)}")

# Step 8: RESET INDEX to avoid indexing issues
file_df = file_df.reset_index(drop=True)

# Step 9: EXTRACT FILE NAME ONLY (with extension)
file_df["file_name_only"] = file_df["rel_path"].apply(lambda x: Path(x).name)

# Step 10: HANDLE CHECKSUM
file_df["DATA_CHECKSUM"] = file_df["DATA_CHECKSUM"].fillna("").astype(str)

# Step 11: DETECT DUPLICATES
file_df["dup_checksum"] = (file_df["DATA_CHECKSUM"] != "") & file_df["DATA_CHECKSUM"].duplicated(keep=False)
file_df["dup_name"] = file_df["file_name_only"].duplicated(keep=False)
file_df["dup_both"] = file_df["dup_checksum"] & file_df["dup_name"]

# Step 12: ASSIGN DUPLICATE GROUP IDs
file_df["dup_group_id"] = 0
current_group_id = 1

# 12a: Group by checksum
for checksum, indices in file_df[file_df["DATA_CHECKSUM"] != ""].groupby("DATA_CHECKSUM").indices.items():
    file_df.loc[indices, "dup_group_id"] = current_group_id
    current_group_id += 1

# 12b: Group by file name (including extension)
for fname, indices in file_df.groupby("file_name_only").indices.items():
    existing_ids = file_df.loc[indices, "dup_group_id"].unique()
    existing_ids = existing_ids[existing_ids != 0]
    if len(existing_ids) > 0:
        file_df.loc[indices, "dup_group_id"] = existing_ids.min()
    else:
        file_df.loc[indices, "dup_group_id"] = current_group_id
        current_group_id += 1

# Step 13: FINAL OUTPUT
output_df = file_df[[
    "rel_path",    # full path
    "DATA_SIZE",
    "DATA_CHECKSUM",
    "dup_checksum",
    "dup_name",
    "dup_both",
    "dup_group_id"
]].copy()

output_df.rename(columns={"rel_path": "file_name", "DATA_CHECKSUM": "checksum"}, inplace=True)

# Step 14: SORT CSV for easier manual inspection
output_df = output_df.sort_values(
    by=["dup_both", "dup_checksum", "dup_name", "dup_group_id", "file_name"],
    ascending=False
)

# Step 15: SAVE OUTPUT
OUT_DIR.mkdir(parents=True, exist_ok=True)
out_file = OUT_DIR / "duplicate_detection.csv"
output_df.to_csv(out_file, index=False)

print(f"Saved structured duplicate file to: {out_file}")
print(f"Total rows in output: {len(output_df)}")