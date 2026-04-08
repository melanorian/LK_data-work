#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ----------------- CONFIGURATION -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")
MAX_LEVEL = 5

# Input files
SUMMARY_FILE = BASE_DIR / f"summarized_inventory_L{MAX_LEVEL}.csv"
DUP_FILE = BASE_DIR / "duplicate_detection.csv"

# Output file
OUT_FILE = BASE_DIR / f"8_summarized_inventory_with_duplicates_L{MAX_LEVEL}.csv"
# ---------------------------------------------------

# Step 1: LOAD DATA
summary_df = pd.read_csv(SUMMARY_FILE)
dup_df = pd.read_csv(DUP_FILE)

print(f"Loaded {len(summary_df)} summarized collections from Step 6")
print(f"Loaded {len(dup_df)} file-level duplicate entries from Step 7")

# Step 2: MAP FILES TO PARENT COLLECTIONS
# Match each file to the deepest summary collection that is a parent of the file
summary_collections = summary_df["collection"].tolist()

def find_parent_collection(file_path):
    """
    Return the deepest matching summary collection that is a parent of the file
    """
    matches = [col for col in summary_collections if file_path.startswith(col)]
    if not matches:
        return None
    # Return the longest match to ensure the deepest parent
    return max(matches, key=len)

dup_df["parent_collection"] = dup_df["file_name"].apply(find_parent_collection)

# Step 3: FILTER OUT FILES NOT MAPPED (optional)
dup_df = dup_df[dup_df["parent_collection"].notna()].copy()
print(f"{len(dup_df)} files mapped to Step 6 collections")

# Step 4: AGGREGATE DUPLICATE INFO PER COLLECTION
agg_dup = dup_df.groupby("parent_collection").agg(
    num_dup_checksum=("dup_checksum", "sum"),
    num_dup_name=("dup_name", "sum"),
    num_dup_both=("dup_both", "sum"),
    num_files_in_dup_check=("file_name", "count"),
    size_dup_checksum=("DATA_SIZE", lambda x: x[dup_df.loc[x.index, "dup_checksum"]].sum()),
    size_dup_name=("DATA_SIZE", lambda x: x[dup_df.loc[x.index, "dup_name"]].sum()),
    size_dup_both=("DATA_SIZE", lambda x: x[dup_df.loc[x.index, "dup_both"]].sum())
).reset_index()

# Step 5: MERGE WITH SUMMARY
merged_df = summary_df.merge(agg_dup, how="left", left_on="collection", right_on="parent_collection")
merged_df.drop(columns=["parent_collection"], inplace=True)

# Step 6: FILL NAs WITH 0 (collections with no duplicates)
for col in ["num_dup_checksum", "num_dup_name", "num_dup_both", "num_files_in_dup_check"]:
    merged_df[col] = merged_df[col].fillna(0).astype(int)

# Step 7: SAVE OUTPUT
merged_df.to_csv(OUT_FILE, index=False)
print(f"Merged inventory with duplicate info saved to: {OUT_FILE}")
print(f"Total collections in output: {len(merged_df)}")