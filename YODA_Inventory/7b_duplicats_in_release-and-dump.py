#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ---------------- CONFIGURATION ----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

INPUT_FILE = BASE_DIR / "duplicate_detection.csv"
OUT_FILE = BASE_DIR / "files_in_both_release_and_dump.csv"
# ----------------------------------------------


# Step 1: LOAD
df = pd.read_csv(INPUT_FILE)

# Step 2: NORMALISE PATH CLASS
df["is_release"] = df["file_name"].str.contains("research-lettuceknow-releases/")
df["is_dump"] = df["file_name"].str.contains("research-lettuceknow/")

# Step 3: FILTER DUPLICATES (important: weak checksum coverage)
dup_df = df[(df["dup_name"] == True) | (df["dup_both"] == True)].copy()

# Step 4: FIND FILES PRESENT IN BOTH AREAS
# group by filename without path
dup_df["basename"] = dup_df["file_name"].apply(lambda x: Path(x).name)

summary = dup_df.groupby("basename").agg(
    in_release=("is_release", "max"),
    in_dump=("is_dump", "max"),
    count=("file_name", "count")
).reset_index()

# Step 5: KEEP ONLY OVERLAP CANDIDATES
candidates = summary[(summary["in_release"] == True) & (summary["in_dump"] == True)]

# Step 6: SAVE
candidates.to_csv(OUT_FILE, index=False)

print(f"Found {len(candidates)} cross-location duplicate file types")
print(f"Saved to {OUT_FILE}")