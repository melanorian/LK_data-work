#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# CONFIGURATION
BASE_DIR = Path("/home/melanie/Documents/LK_data/test-set_inventory_eGWAS_summary_tables")

# FIND CSV FILES
csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))
print(f"Found {len(csv_files)} CSV files:")
for f in csv_files:
    print(f" - {f}")

# READ CSVs AND CHECK COLUMNS
df_list = []
columns_sets = []

for f in csv_files:
    df = pd.read_csv(f)
    df["source_dir"] = f.parent.name
    df_list.append(df)
    columns_sets.append(set(df.columns))

# CHECK FOR COLUMN CONSISTENCY
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

# IF ALL GOOD, COMBINE
if not inconsistent_files:
    full_df = pd.concat(df_list, ignore_index=True)
    print(f"Total rows imported: {len(full_df)}")
    print(full_df.head())