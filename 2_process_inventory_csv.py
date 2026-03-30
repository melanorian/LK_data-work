#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ----------------- CONFIGURATION VARIABLES -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/test-set_inventory_eGWAS_summary_tables")
IGNORE_PRE = "/nluu6p/home/"  # prefix to ignore in paths
MAX_LEVEL = 5  # maximum level of subcollection to aggregate
# -----------------------------------------------------------

# Step 1: FIND CSV FILES
csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))
print(f"Found {len(csv_files)} CSV files:")
for f in csv_files:
    print(f" - {f}")

# Step 2: READ CSVS AND CHECK COLUMNS
df_list = []
columns_sets = []

for f in csv_files:
    df = pd.read_csv(f)
    df["source_dir"] = f.parent.name
    df_list.append(df)
    columns_sets.append(set(df.columns))

# Step 3: CHECK FOR COLUMN CONSISTENCY
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

# Step 4: IF ALL GOOD, COMBINE CSVs
if not inconsistent_files:
    full_df = pd.concat(df_list, ignore_index=True)

    # --- FIX: rename column to match the script ---
    full_df.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)
    
    # Ensure DATA_SIZE is numeric
    full_df["DATA_SIZE"] = pd.to_numeric(full_df["DATA_SIZE"], errors="coerce").fillna(0).astype(int)
    
    print(f"Total rows imported: {len(full_df)}")
    print(full_df.head())

    # Step 5: NORMALIZE PATHS RELATIVE TO IGNORE_PREFIX
    full_df["rel_path"] = full_df["COLL_NAME"].apply(lambda x: str(x).replace(IGNORE_PRE, "", 1))
    full_df["path_parts"] = full_df["rel_path"].apply(lambda x: Path(x).parts)

    # Step 6: DEFINE SUBCOLLECTION KEY AT MAX LEVEL
    def get_subcollection_key(parts, level):
        # take first 'level' directories as key; if fewer dirs, take all
        if len(parts) < level:
            return "/".join(parts[:-1])  # exclude file name
        return "/".join(parts[:level])

    full_df["subcollection_max"] = full_df["path_parts"].apply(lambda p: get_subcollection_key(p, MAX_LEVEL))

# Step 7: AGGREGATE DATA FOR MAX LEVEL
df_max = full_df.groupby("subcollection_max").agg(
    collection_size_bytes=("DATA_SIZE", "sum"),
    num_files=("COLL_NAME", "count")  # was DATA_NAME, now COLL_NAME
).reset_index()

# Step 8: CONVERT SIZE TO GB AND TB
df_max["collection_size_GB"] = df_max["collection_size_bytes"] / 1_000_000_000
df_max["collection_size_TB"] = df_max["collection_size_bytes"] / 1_000_000_000_000

# Step 9: RENAME COLUMNS FOR CLARITY
df_max = df_max.rename(columns={"subcollection_max": "collection"})

# Step 10: QUICK CHECK
print("Summary table for max-level subcollections:")
print(df_max.head())