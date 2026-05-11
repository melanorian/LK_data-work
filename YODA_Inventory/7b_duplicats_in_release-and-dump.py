#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

INPUT_FILE = BASE_DIR / "7_duplicate_detection.csv"
OUT_FILE = BASE_DIR / "7b_delete_duplicates.csv"

df = pd.read_csv(INPUT_FILE)

# ---------------- SAFETY CHECK ----------------
required_cols = {"file_path", "dup_group_id", "storage_location"}
missing = required_cols - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# ---------------- PRIORITY RULE ----------------
def priority(path):
    if "data-release_V2" in path:
        return 3
    elif "data-release_V1" in path:
        return 2
    else:
        return 1

df["priority"] = df["file_path"].astype(str).apply(priority)

# ---------------- GROUP MAX PRIORITY ----------------
df["max_priority_in_group"] = df.groupby("dup_group_id")["priority"].transform("max")

# ---------------- DELETE RULE ----------------
df["delete_duplicate"] = df["priority"] < df["max_priority_in_group"]

breakpoint()

# ---------------- OUTPUT ----------------
output_df = df.copy()

output_df = output_df.sort_values(
    by=["dup_group_id", "priority", "file_path"],
    ascending=[True, False, True]
)

output_df.to_csv(OUT_FILE, index=False)

print(f"Saved to: {OUT_FILE}")
print(f"Total rows: {len(output_df)}")
print(f"Marked for deletion: {output_df['delete_duplicate'].sum()}")