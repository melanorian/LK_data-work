import pandas as pd
from pathlib import Path
import json

# Configuration
IGNORE_PRE = "/nluu6p/home/"
MAX_LEVEL = 5
BASE_DIR = Path("/home/melanie/Documents/LK_data/inventory_data")
OUT_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")  # Can change if desired

# --- Step 1: Locate all inventory CSVs recursively ---
csv_files = list(BASE_DIR.rglob("inventory.csv"))
if not csv_files:
    raise FileNotFoundError(f"No inventory CSVs found in {BASE_DIR}")

dfs = []
for f in csv_files:
    df = pd.read_csv(f)
    
    # --- Step 2: Fix inconsistent headers ---
    path_col_candidates = ["COLL_NAME", "DATA_NAME", "COLL_NAME/DATA_NAME"]
    for col in path_col_candidates:
        if col in df.columns:
            df.rename(columns={col: "COLL_NAME"}, inplace=True)
            break
    else:
        print(f"Skipping {f.name} (no recognized path column)")
        continue
    
    dfs.append(df)

# Combine all CSVs
full_df = pd.concat(dfs, ignore_index=True)

# --- Step 3: Normalize paths ---
full_df["REL_PATH"] = full_df["COLL_NAME"].str.replace(IGNORE_PRE, "", regex=False)
full_df["path_parts"] = full_df["REL_PATH"].str.split("/")

# --- Step 4: Extract file extension (handles multi-part like .tsv.gz) ---
def get_extension(filename):
    fname = Path(filename).name
    parts = fname.split(".")
    if len(parts) <= 1:
        return "no_ext"
    if parts[-1] in ["gz", "bz2", "zip"] and len(parts) > 2:
        return ".".join(parts[-2:])
    return parts[-1]

full_df["EXT"] = full_df["REL_PATH"].apply(get_extension)

# --- Step 5: Aggregate by directory branches up to MAX_LEVEL ---
def get_branch(parts):
    return "/".join(parts[:MAX_LEVEL]) if len(parts) >= MAX_LEVEL else "/".join(parts)

full_df["BRANCH"] = full_df["path_parts"].apply(get_branch)

agg_list = []
for branch, group in full_df.groupby("BRANCH"):
    num_files = len(group)
    file_types = group["EXT"].value_counts().to_dict()
    
    agg_list.append({
        "BRANCH": branch,
        "num_files": num_files,
        "file_types": json.dumps(file_types)
    })

summary_df = pd.DataFrame(agg_list)

# --- Step 6: Save summary ---
OUT_DIR.mkdir(parents=True, exist_ok=True)

output_file = OUT_DIR / f"file-type_inventory_L{MAX_LEVEL}.csv"
summary_df.to_csv(output_file, index=False)

print(f"Summary saved to {output_file}")