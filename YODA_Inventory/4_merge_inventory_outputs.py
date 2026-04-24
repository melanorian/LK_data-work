#!/usr/bin/env python

import pandas as pd
from pathlib import Path
import json

# ----------------- CONFIGURATION -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")
MAX_LEVEL = 5
OUT_FILE = BASE_DIR / f"merged_inventory_L{MAX_LEVEL}.csv"
FILETYPE_SUMMARY = BASE_DIR / "file-type_summary_L4.csv"  # <- file with descriptions
# ------------------------------------------------

# --- Step 1: Identify relevant files ---
filetype_file = BASE_DIR / f"file-type_inventory_L{MAX_LEVEL}.csv"
subcollection_file = BASE_DIR / f"subcollection_summary_L{MAX_LEVEL}.csv"

for f in [filetype_file, subcollection_file]:
    if not f.exists():
        raise FileNotFoundError(f"Missing: {f}")

print(f"Using:\n - {filetype_file}\n - {subcollection_file}")

# --- Step 2: Load data ---
df_types = pd.read_csv(filetype_file)
df_sizes = pd.read_csv(subcollection_file)

# --- Step 3: Standardize column names ---
df_types = df_types.rename(columns={"BRANCH": "collection"})

# --- Step 4: Check uniqueness of keys ---
if df_types["collection"].duplicated().any():
    print("WARNING: duplicates in file-type table")

if df_sizes["collection"].duplicated().any():
    print("WARNING: duplicates in size table")

# --- Step 4.5: Load file type descriptions if file exists ---
if FILETYPE_SUMMARY.exists():
    df_desc = pd.read_csv(FILETYPE_SUMMARY)
    # Create mapping: file_type -> description
    FILETYPE_DESC = pd.Series(df_desc.content.values, index=df_desc.file_type).to_dict()
else:
    FILETYPE_DESC = {}  # empty dict, unknown types will be "NA"

# --- Step 5: Merge ---
merged_df = pd.merge(
    df_sizes,
    df_types[["collection", "file_types"]],
    on="collection",
    how="outer",
    indicator=True
)

# --- Step 6: Inspect merge quality ---
print("\nMerge status:")
print(merged_df["_merge"].value_counts())

mismatch = merged_df[merged_df["_merge"] != "both"]
if not mismatch.empty:
    print("\nWARNING: Some rows did not match between files:")
    print(mismatch.head())

# --- Step 7: Sort for readability ---
merged_df = merged_df.sort_values("collection").reset_index(drop=True)

# Drop merge indicator
merged_df = merged_df.drop(columns=["_merge"])

# --- Step 8: Add file type description column ---
def map_unique_descriptions(ft_json_str):
    """
    Convert a JSON string of file types to a JSON array of unique descriptions.
    Keeps order, removes duplicates.
    """
    try:
        ft_dict = json.loads(ft_json_str)
    except (json.JSONDecodeError, TypeError):
        return "[]"
    
    seen = set()
    unique_desc = []
    for ft in ft_dict.keys():
        desc = FILETYPE_DESC.get(ft, "NA")
        if desc not in seen:
            seen.add(desc)
            unique_desc.append(desc)
    return json.dumps(unique_desc)

merged_df["file_type_description"] = merged_df["file_types"].apply(map_unique_descriptions)

# --- Step 9: Save result ---
merged_df.to_csv(OUT_FILE, index=False)
print(f"Saved merged file to: {OUT_FILE}")