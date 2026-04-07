#!/usr/bin/env python

import pandas as pd
from pathlib import Path
import json
from collections import Counter

# ----------------- CONFIGURATION -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")
MAX_LEVEL = 5

INPUT_FILE = BASE_DIR / f"merged_inventory_with_docs_L{MAX_LEVEL}.csv"
OUT_FILE = BASE_DIR / f"summarized_inventory_L{MAX_LEVEL}.csv"
# --------------------------------------------------

# Step 1: LOAD DATA
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {len(df)} rows")

# Step 1a: Ensure documentation columns exist
required_cols = ["README", "log", "config", "metadata"]
for col in required_cols:
    if col not in df.columns:
        print(f"Warning: {col} column missing, adding zeros")
        df[col] = 0

# Step 2: IDENTIFY FILE-LEVEL ROWS
df["is_file"] = df["collection"].apply(lambda x: Path(str(x)).suffix != "")

# Step 3: REMOVE PRE-AGGREGATED COLLECTION ROWS
collections_with_files = set(df[df["is_file"]]["collection"].apply(lambda x: str(Path(x).parent)))
df = df[~((~df["is_file"]) & (df["collection"].isin(collections_with_files)))].copy()

# Step 4: SUMMARIZED COLLECTION PATHS
df["summarized_collection"] = df.apply(
    lambda row: str(Path(row["collection"]).parent) if row["is_file"] else row["collection"],
    axis=1
)

# Step 5: PREPARE FILE TYPE DICTS
def safe_load_dict(x):
    if pd.isna(x) or x == "" or x == "[]":
        return {}
    try:
        return json.loads(x)
    except Exception:
        return {}

df["file_types_dict"] = df["file_types"].apply(safe_load_dict)

# Step 5a: Ensure numeric columns
numeric_cols = ["collection_size_bytes", "num_files", "README", "log", "config", "metadata"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Step 6: AGGREGATION FUNCTION FOR FILE TYPES
def merge_dicts(series):
    total = Counter()
    for d in series:
        total.update(d)
    return dict(total)

# Step 7: GROUP AND AGGREGATE
agg_df = df.groupby("summarized_collection").agg({
    "collection_size_bytes": "sum",
    "num_files": "sum",
    "README": "sum",
    "log": "sum",
    "config": "sum",
    "metadata": "sum",
    "file_types_dict": merge_dicts
}).reset_index()

# Step 8: RECOMPUTE SIZE METRICS
agg_df["collection_size_GB"] = agg_df["collection_size_bytes"] / 1e9
agg_df["collection_size_TB"] = agg_df["collection_size_bytes"] / 1e12

# Step 9: FINAL CLEANUP
agg_df.rename(columns={"summarized_collection": "collection"}, inplace=True)

# Convert file_types dict back to JSON string
agg_df["file_types"] = agg_df["file_types_dict"].apply(json.dumps)
agg_df.drop(columns=["file_types_dict"], inplace=True)

# Step 10: REORDER COLUMNS
agg_df = agg_df[
    ["collection", "num_files", "collection_size_bytes",
     "collection_size_GB", "collection_size_TB",
     "README", "log", "config", "metadata", "file_types"]
]

# Step 11: KEEP ONLY DEEPEST COLLECTIONS
collections = agg_df["collection"].tolist()

# Keep only collections that are not fully contained in another collection
to_keep = [col for i, col in enumerate(collections)
           if not any(other != col and col in other for other in collections)]

agg_df = agg_df[agg_df["collection"].isin(to_keep)].copy()

# Step 12: SAVE OUTPUT
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
agg_df.to_csv(OUT_FILE, index=False)

print(f"summarized dataset saved to: {OUT_FILE}")
print(f"Total rows after filtering deepest collections: {len(agg_df)}")