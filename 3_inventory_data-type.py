#!/usr/bin/env python

import pandas as pd
from pathlib import Path
from collections import Counter
import json

# ----------------- CONFIGURATION VARIABLES -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/test-set_inventory_eGWAS_summary_tables")
OUT_DIR = Path("/home/melanie/Documents/LK_data/test-set_inventory_eGWAS_summary_tables")
IGNORE_PRE = "/nluu6p/home/"  # prefix to ignore in paths
MIN_FILE_FRACTION = 0.8  # threshold to define first meaningful collection
# -----------------------------------------------------------

# Step 1: FIND CSV FILES
csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))
print(f"Found {len(csv_files)} CSV files:")
for f in csv_files:
    print(f" - {f}")

# Step 2: READ CSVS AND FIX HEADER
df_list = []
columns_sets = []

for f in csv_files:
    with open(f, "r") as fh:
        header_line = fh.readline().strip()
        fixed_header = header_line.replace("COLL_NAME,DATA_NAME", "COLL_NAME/DATA_NAME").split(",")
    df = pd.read_csv(f, header=0, names=fixed_header, skiprows=1)
    df["source_dir"] = f.parent.name
    df_list.append(df)
    columns_sets.append(set(df.columns))

# Step 3: CHECK COLUMN CONSISTENCY
first_columns = columns_sets[0]
inconsistent_files = []
for i, cols in enumerate(columns_sets):
    if cols != first_columns:
        inconsistent_files.append(csv_files[i])

if inconsistent_files:
    print("The following files have different columns:")
    for f in inconsistent_files:
        print(f" - {f}")
else:
    print("All inventory CSVs have consistent columns.")

# Step 4: COMBINE CSVS AND CLEAN DATA
if not inconsistent_files:
    full_df = pd.concat(df_list, ignore_index=True)

    full_df.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)
    full_df["DATA_SIZE"] = pd.to_numeric(full_df["DATA_SIZE"], errors="coerce").fillna(0).astype(int)

    # Normalize paths relative to IGNORE_PRE
    full_df["rel_path"] = full_df["COLL_NAME"].apply(lambda x: str(x).replace(IGNORE_PRE, "", 1))
    full_df["path_parts"] = full_df["rel_path"].apply(lambda x: Path(x).parts)

    print(f"Total rows imported: {len(full_df)}")

    # Step 5: BUILD DIRECTORY TREE
    dir_counts = {}
    for idx, row in full_df.iterrows():
        parts = row["path_parts"]
        for level in range(1, len(parts)):
            dir_path = "/".join(parts[:level])
            dir_counts.setdefault(dir_path, {"files": 0, "total": 0})
            dir_counts[dir_path]["total"] += 1
        # last level is the file
        file_path = "/".join(parts)
        parent_dir = "/".join(parts[:-1])
        dir_counts.setdefault(parent_dir, {"files": 0, "total": 0})
        dir_counts[parent_dir]["files"] += 1
        dir_counts[parent_dir]["total"] += 1

    # Step 6: DETERMINE FIRST MEANINGFUL COLLECTION PER FILE
    def find_first_meaningful(parts):
        for level in range(1, len(parts)):
            dir_path = "/".join(parts[:level])
            info = dir_counts.get(dir_path, {"files": 0, "total": 1})
            fraction = info["files"] / info["total"] if info["total"] > 0 else 0
            if fraction >= MIN_FILE_FRACTION:
                return dir_path
        # fallback: top-level
        return "/".join(parts[:-1])

    # assign first meaningful collection per file
    full_df["first_meaningful_collection"] = full_df["path_parts"].apply(find_first_meaningful)

    # Step 6b: ENSURE ALL FILES BELOW THIS COLLECTION ARE ASSIGNED TO IT
    # This means we replace first_meaningful_collection with the canonical path
    canonical_map = {}

    # build a unique set of first meaningful collections
    unique_collections = full_df["first_meaningful_collection"].unique()

    # assign every file to the **topmost collection that is a prefix of its path**
    def get_canonical_collection(path):
        for col in unique_collections:
            if str(path).startswith(col):
                return col
        return str(path)  # fallback

    full_df["first_meaningful_collection"] = full_df["rel_path"].apply(get_canonical_collection)

    # Step 7: AGGREGATE SUMMARY
    def file_extensions_counter(files):
        exts = []
        for f in files:
            if ".gz" in f:
                exts.append(".gz")
            elif "." in f:
                exts.append("." + f.split(".")[-1])
            else:
                exts.append("no_ext")
        return dict(Counter(exts))

    summary_df = full_df.groupby("first_meaningful_collection").agg(
        collection_size_bytes=("DATA_SIZE", "sum"),
        num_files=("COLL_NAME", "count"),
        file_types=("COLL_NAME", lambda x: json.dumps(file_extensions_counter(x)))
    ).reset_index()

    summary_df["collection_size_GB"] = summary_df["collection_size_bytes"] / 1_000_000_000
    summary_df["collection_size_TB"] = summary_df["collection_size_bytes"] / 1_000_000_000_000

    # Step 8: QUICK CHECK
    print("Summary table for first meaningful collections:")
    print(summary_df.head())

    # Step 9: SAVE SUMMARY TABLE
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / "subcollection_summary_first_meaningful_fixed.csv"
    summary_df.to_csv(out_file, index=False, sep=",")
    print(f"Saved first meaningful collection summary to: {out_file}")