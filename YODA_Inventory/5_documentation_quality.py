#!/usr/bin/env python

import pandas as pd
from pathlib import Path

# ----------------- CONFIGURATION -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/inventory_data")
REPORT_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

MAX_LEVEL = 5

MERGED_FILE = REPORT_DIR / f"merged_inventory_L{MAX_LEVEL}.csv"
OUT_FILE = REPORT_DIR / f"merged_inventory_with_docs_L{MAX_LEVEL}.csv"
# ------------------------------------------------


# STEP 1: LOAD MERGED INVENTORY (COLLECTION LEVEL)
# ------------------------------------------------
df_collections = pd.read_csv(MERGED_FILE)
print(f"Loaded merged inventory: {len(df_collections)} collections")


# STEP 2: LOAD FILE-LEVEL INVENTORY CSVs
# ------------------------------------------------
csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))
print(f"Found {len(csv_files)} inventory CSV files")

df_list = []

for f in csv_files:
    with open(f, "r") as fh:
        header_line = fh.readline().strip()
        fixed_header = header_line.replace(
            "COLL_NAME,DATA_NAME",
            "COLL_NAME/DATA_NAME"
        ).split(",")

    df = pd.read_csv(f, header=0, names=fixed_header, skiprows=1)
    df_list.append(df)

df_files = pd.concat(df_list, ignore_index=True)

# Standardize column name
df_files.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)

print(f"Loaded file-level rows: {len(df_files)}")


# STEP 3: PREPARE COLLECTION KEY (MATCH STEP 4)
# IMPORTANT: must match how you defined collection in previous scripts

def get_collection_key(path, level):
    parts = Path(path.replace("/nluu6p/home/", "", 1)).parts
    if len(parts) < level:
        return "/".join(parts[:-1])
    return "/".join(parts[:level])

df_files["collection"] = df_files["COLL_NAME"].apply(
    lambda x: get_collection_key(x, MAX_LEVEL)
)

# STEP 4: CLASSIFY INFORMATIVE FILES
# ------------------------------------------------
def classify_info_file(fname: str) -> dict:
    fname_lower = fname.lower()

    return {
        "README": int("readme" in fname_lower),

        # log files (strict: extensions only to avoid false positives)
        "log": int(fname_lower.endswith((".log", ".out", ".err"))),

        # config files
        "config": int(
            fname_lower.endswith((".cfg", ".ini", ".yaml", ".yml"))
            or "config" in fname_lower
        ),

        # metadata files
        "metadata": int(
            fname_lower.endswith((".json", ".xml", ".tsv", ".csv"))
            or "metadata" in fname_lower
        ),
    }

# Extract file names
df_files["file_name"] = df_files["COLL_NAME"].apply(lambda x: Path(x).name)

# Apply classification
df_info = df_files["file_name"].apply(classify_info_file).apply(pd.Series)

# Merge back
df_files = pd.concat([df_files, df_info], axis=1)


# STEP 5: AGGREGATE PER COLLECTION
# ------------------------------------------------
df_summary = (
    df_files.groupby("collection")[["README", "log", "config", "metadata"]]
    .sum()
    .reset_index()
)

print("Aggregated documentation indicators per collection")


# STEP 6: MERGE WITH EXISTING COLLECTION DATA
# ------------------------------------------------
df_final = pd.merge(
    df_collections,
    df_summary,
    on="collection",
    how="left"
)

# Fill NaNs (collections without matches)
for col in ["README", "log", "config", "metadata"]:
    df_final[col] = df_final[col].fillna(0).astype(int)


# STEP 7: SAVE OUTPUT
# ------------------------------------------------
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df_final.to_csv(OUT_FILE, index=False)

print(f"Saved enriched inventory to: {OUT_FILE}")