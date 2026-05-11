#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ---------------- CONFIGURATION ----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

INPUT_FILE = BASE_DIR / "duplicate_detection.csv"
OUT_FILE = BASE_DIR / "7b_files_in_both_release_and_dump.csv"
# ----------------------------------------------


# Step 1 — LOAD (DO NOT CLEAN EARLY, as requested)
df = pd.read_csv(INPUT_FILE)

# Step 2 — FLAG LOCATION
df["is_release"] = df["file_name"].str.contains("research-lettuceknow-releases/", na=False)
df["is_dump"] = df["file_name"].str.contains("research-lettuceknow/", na=False)

# Step 3 — DEFINE DUPLICATES (UPDATED CORRECTLY)
df["is_duplicate"] = (
    (df["dup_name"] == True) |
    (df["dup_both"] == True) |
    (df["dup_checksum"] == True)
)

dup_df = df[df["is_duplicate"]].copy()

# =========================================================
# STEP 4 — GROUP BY TRUE ID (dup_group_id)
# =========================================================

# Global duplicate size per group ID (from FULL dataset, not filtered)
group_sizes = (
    df.groupby("dup_group_id")
      .size()
      .rename("duplicate_group_size")
      .reset_index()
)

dup_df = dup_df.merge(group_sizes, on="dup_group_id", how="left")

# Step 5 — CROSS LOCATION SUMMARY per group ID
summary = dup_df.groupby("dup_group_id").agg(
    in_release=("is_release", "max"),
    in_dump=("is_dump", "max"),
    count=("file_name", "count")
).reset_index()

# Step 6 — KEEP ONLY CROSS-LOCATION GROUPS
valid_groups = summary[
    (summary["in_release"] == True) &
    (summary["in_dump"] == True)
]["dup_group_id"]

# Step 7 — KEEP ONLY DUMP SIDE ROWS (your requirement)
result = dup_df[
    (dup_df["dup_group_id"].isin(valid_groups)) &
    (dup_df["is_dump"] == True)
].copy()

# Step 8 — SAVE FULL DETAIL (no loss of metadata)
result.to_csv(OUT_FILE, index=False)

print(f"Cross-location duplicate groups: {len(valid_groups)}")
print(f"Dump-side rows written: {len(result)}")
print(f"Output: {OUT_FILE}")