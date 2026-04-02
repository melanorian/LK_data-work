#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ----------------- CONFIGURATION VARIABLES -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/inventory_data")
OUT_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

TARGET_COLLECTION = "research-lettuceknow/processed_data/rnaseq"

OUT_FILE = OUT_DIR / "optional1_rnaseq_file_level_inventory.csv"
# -----------------------------------------------------------

# Step 1: FIND CSV FILES
csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))
print(f"Found {len(csv_files)} CSV files")

# Step 2: READ + FIX HEADERS
df_list = []

for f in csv_files:
    with open(f, "r") as fh:
        header_line = fh.readline().strip()
        fixed_header = header_line.replace(
            "COLL_NAME,DATA_NAME",
            "COLL_NAME/DATA_NAME"
        ).split(",")

    df = pd.read_csv(f, header=0, names=fixed_header, skiprows=1)
    df_list.append(df)

# Step 3: COMBINE
full_df = pd.concat(df_list, ignore_index=True)

# Standardize column name
full_df.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)

# Step 4: NORMALIZE PATH (remove prefix)
full_df["rel_path"] = full_df["COLL_NAME"].str.replace(
    "/nluu6p/home/", "", 1
)

# Step 5: FILTER TARGET COLLECTION
df_target = full_df[
    full_df["rel_path"].str.startswith(TARGET_COLLECTION)
].copy()

print(f"Rows in target collection: {len(df_target)}")

# Step 6: SAVE OUTPUT
OUT_DIR.mkdir(parents=True, exist_ok=True)
df_target.to_csv(OUT_FILE, index=False)

print(f"Saved to: {OUT_FILE}")