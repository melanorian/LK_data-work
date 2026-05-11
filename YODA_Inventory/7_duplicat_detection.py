#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

BASE_DIR = Path("/home/melanie/Documents/LK_data/inventory_data")
OUT_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")
IGNORE_PRE = "/nluu6p/home/"

OUT_DIR.mkdir(parents=True, exist_ok=True)

out_file = OUT_DIR / "7_duplicate_detection.csv"

csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))
print(f"Found {len(csv_files)} CSV files:")
for f in csv_files:
    print(f" - {f}")

df_list = []
columns_sets = []

for f in csv_files:
    with open(f, "r") as fh:
        header_line = fh.readline().strip()
        fixed_header = header_line.replace(
            "COLL_NAME,DATA_NAME",
            "COLL_NAME/DATA_NAME"
        ).split(",")

    df = pd.read_csv(
        f,
        header=0,
        names=fixed_header,
        skiprows=1,
        dtype=str
    )

    df["source_dir"] = f.parent.name
    df_list.append(df)
    columns_sets.append(set(df.columns))

first_columns = columns_sets[0]
for i, cols in enumerate(columns_sets):
    if cols != first_columns:
        print(f"Inconsistent columns in: {csv_files[i]}")
        exit()

print("All inventory CSVs consistent.")

full_df = pd.concat(df_list, ignore_index=True)
full_df.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)

full_df["DATA_SIZE"] = pd.to_numeric(
    full_df.get("DATA_SIZE", 0),
    errors="coerce"
).fillna(0).astype(int)

print(f"Total rows imported: {len(full_df)}")

full_df["rel_path"] = full_df["COLL_NAME"].apply(
    lambda x: str(x).replace(IGNORE_PRE, "", 1)
)

full_df["is_file"] = full_df["rel_path"].apply(lambda x: "." in Path(x).name)
file_df = full_df[full_df["is_file"]].copy()

file_df["file_path"] = file_df["COLL_NAME"].astype(str)
file_df["basename"] = file_df["file_path"].apply(lambda x: Path(x).name)

file_df["DATA_CHECKSUM"] = file_df["DATA_CHECKSUM"].fillna("").astype(str)

file_df["identity"] = file_df["DATA_CHECKSUM"].where(
    file_df["DATA_CHECKSUM"] != "",
    file_df["basename"]
)

file_df["dup_checksum"] = (
    (file_df["DATA_CHECKSUM"] != "") &
    file_df["DATA_CHECKSUM"].duplicated(keep=False)
)

file_df["dup_name"] = file_df["basename"].duplicated(keep=False)

file_df["dup_any"] = file_df["identity"].duplicated(keep=False)

file_df["duplicate_group_size"] = file_df.groupby("identity")["identity"].transform("size")
file_df["dup_group_id"] = file_df.groupby("identity").ngroup() + 1

file_df["storage_location"] = file_df["file_path"].apply(
    lambda x: "research-lettuceknow-releases" if "research-lettuceknow-releases/" in x else "research-lettuceknow"
)

output_df = file_df[[
    "file_path",
    "basename",
    "DATA_SIZE",
    "DATA_CHECKSUM",
    "storage_location",
    "dup_name",
    "dup_checksum",
    "dup_any",
    "dup_group_id",
    "duplicate_group_size"
]].copy()

output_df = output_df.sort_values(
    by=["duplicate_group_size", "dup_group_id", "file_path"],
    ascending=False
)

output_df.to_csv(out_file, index=False)

print(f"Saved to: {out_file}")
print(f"Total rows: {len(output_df)}")
print(f"Duplicate groups: {output_df['dup_group_id'].nunique()}")