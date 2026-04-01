#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ----------------- CONFIGURATION -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")
MAX_LEVEL = 5
OUT_FILE = BASE_DIR / f"merged_inventory_L{MAX_LEVEL}.csv"
# ------------------------------------------------

# --- Step 1: Identify relevant files ---
filetype_file = BASE_DIR / f"file-type_inventory_L{MAX_LEVEL}.csv"
subcollection_file = BASE_DIR / f"subcollection_summary_L{MAX_LEVEL}.csv"

if not filetype_file.exists():
    raise FileNotFoundError(f"Missing: {filetype_file}")

if not subcollection_file.exists():
    raise FileNotFoundError(f"Missing: {subcollection_file}")

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

# --- Step 6: Merge ---
merged_df = pd.merge(
    df_sizes,
    df_types[["collection", "file_types"]],
    on="collection",
    how="outer",   # keeps everything (safer)
    indicator=True
)

# --- Step 7: Inspect merge quality ---
print("\nMerge status:")
print(merged_df["_merge"].value_counts())

# Optional: inspect mismatches
mismatch = merged_df[merged_df["_merge"] != "both"]
if not mismatch.empty:
    print("\nWARNING: Some rows did not match between files:")
    print(mismatch.head())

# --- Step 7.5: Sort for readability ---
merged_df = merged_df.sort_values("collection").reset_index(drop=True)

# Drop merge indicator if not needed
merged_df = merged_df.drop(columns=["_merge"])

# --- Step 8: Save result ---
merged_df.to_csv(OUT_FILE, index=False)