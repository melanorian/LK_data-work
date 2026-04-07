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


required_cols = ["README", "log", "config", "metadata"]
for col in required_cols:
    if col not in df.columns:
        print(f"Warning: {col} column missing, adding zeros")
        df[col] = 0

# Step 2: IDENTIFY FILE-LEVEL ROWS
df["is_file"] = df["collection"].apply(lambda x: Path(str(x)).suffix != "")


# Step 3: SUMMARIZED COLLECTION PATHS
df["summarized_collection"] = df.apply(
    lambda row: str(Path(row["collection"]).parent)
    if row["is_file"]
    else row["collection"],
    axis=1
)


# Step 4: PREPARE FILE TYPE DICTS
def safe_load_dict(x):
    if pd.isna(x) or x == "" or x == "[]":
        return {}
    try:
        return json.loads(x)
    except Exception:
        return {}


df["file_types_dict"] = df["file_types"].apply(safe_load_dict)


# Step 5: AGGREGATION FUNCTION FOR FILE TYPES
def merge_dicts(series):
    total = Counter()
    for d in series:
        total.update(d)
    return dict(total)


# Step 6: GROUP AND AGGREGATE
agg_df = df.groupby("summarized_collection").agg({
    "collection_size_bytes": "sum",
    "num_files": "sum",
    "README": "sum",
    "log": "sum",
    "config": "sum",
    "metadata": "sum",
    "file_types_dict": merge_dicts
}).reset_index()


# Step 7: RECOMPUTE SIZE METRICS
agg_df["collection_size_GB"] = agg_df["collection_size_bytes"] / 1e9
agg_df["collection_size_TB"] = agg_df["collection_size_bytes"] / 1e12


# Step 8: FINAL CLEANUP
agg_df.rename(columns={"summarized_collection": "collection"}, inplace=True)

# Convert dict back to JSON string
agg_df["file_types"] = agg_df["file_types_dict"].apply(json.dumps)

# Drop helper column
agg_df.drop(columns=["file_types_dict"], inplace=True)


# Step 9: SAVE OUTPUT
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
agg_df.to_csv(OUT_FILE, index=False)

print(f"summarized dataset saved to: {OUT_FILE}")
print(f"Total rows after summarization: {len(agg_df)}")