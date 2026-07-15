#!/usr/bin/env python3

import pandas as pd
from pathlib import Path

# ----------------- CONFIGURATION -----------------

BASE_DIR = Path("/home/melanie/Documents/LK_data/inventory_data")
IGNORE_PRE = "/nluu6p/home/"

# -------------------------------------------------
# Step 1: MANUAL ALD REGISTRY (single source of truth)
# -------------------------------------------------

ALD_LIST = [
    "ALD10469","ALD10486","ALD11088","ALD11419",
    "ALD4378","ALD4379","ALD5442","ALD5849",
    "ALD6230","ALD6371","ALD6682","ALD6683","ALD6684",
    "ALD6742","ALD6742_additional_sequencing_Feb2022",
    "ALD6742_additional_sequencing_May2022_1",
    "ALD6742_additional_sequencing_May2022_2",
    "ALD6760","ALD6978","ALD6978_additional-sequencing_May2022",
    "ALD6979","ALD7153","ALD7161","ALD7439","ALD7440","ALD7922",
    "ALD8538","ALD8718","ALD8718_additional_sequencing_Oct2023",
    "ALD8719","ALD8720"
]

# -------------------------------------------------
# Step 2: LOAD INVENTORY CSVs
# -------------------------------------------------

csv_files = list(BASE_DIR.glob("inventory_*/inventory.csv"))

print(f"Found {len(csv_files)} inventory CSVs")

df_list = []

for f in csv_files:
    with open(f, "r") as fh:
        header_line = fh.readline().strip()
        fixed_header = header_line.replace(
            "COLL_NAME,DATA_NAME",
            "COLL_NAME/DATA_NAME"
        ).split(",")

    df = pd.read_csv(
        f,
        header=0,
        names=fixed_header,
        skiprows=1,
        dtype=str
    )

    df["source_dir"] = f.parent.name
    df_list.append(df)

# combine
full_df = pd.concat(df_list, ignore_index=True)
print(f"Total inventory rows loaded: {len(full_df)}")

full_df.rename(columns={"COLL_NAME/DATA_NAME": "COLL_NAME"}, inplace=True)

full_df["COLL_NAME"] = full_df["COLL_NAME"].astype(str)

# -------------------------------------------------
# Step 3: FILTER USING DIRECT STRING MATCH
# -------------------------------------------------

# match any ALD token inside path
pattern = "|".join(ALD_LIST)

df_filtered = full_df[
    full_df["COLL_NAME"].str.contains(pattern, na=False)
].copy()

print(f"Matching inventory rows: {len(df_filtered)}")
print(f"Matching inventory rows: {len(df_filtered)} of {len(full_df)} total rows")

# -------------------------------------------------
# Step 4: ASSIGN ALD_id (NO REGEX — PURE STRING MATCH)
# -------------------------------------------------

def find_ald(path):
    for ald in ALD_LIST:
        if ald in str(path):
            return ald
    return None

df_filtered["ALD_id"] = df_filtered["COLL_NAME"].apply(find_ald)

# -------------------------------------------------
# Step 5: FINAL DATAFRAME
# -------------------------------------------------

df_ALD_v1 = df_filtered[[
    "COLL_NAME",
    "DATA_SIZE",
    "DATA_REPL_NUM",
    "DATA_CHECKSUM",
    "source_dir",
    "ALD_id"
]].copy()

df_ALD_v1["DATA_SIZE"] = pd.to_numeric(
    df_ALD_v1["DATA_SIZE"],
    errors="coerce"
).fillna(0)

# ----------------- DEBUG SAMPLE EXPORT -----------------

head_sample = df_ALD_v1.head(500)
tail_sample = df_ALD_v1.tail(500)

debug_sample = pd.concat([head_sample, tail_sample], ignore_index=True)

debug_file = "/home/melanie/Documents/LK_data/LK_inventory_report/11_ALD_sample_1000rows.csv"
debug_sample.to_csv(debug_file, index=False)

print(f"Saved debug sample (head+tail, 1000 rows) to: {debug_file}")

# -------------------------------------------------
# Step 6: QUICK CHECK
# -------------------------------------------------

print(df_ALD_v1.head())
print(f"Final ALD-linked rows: {len(df_ALD_v1)}")
print(f"Unique ALDs in output: {df_ALD_v1['ALD_id'].nunique()}")

# =========================================================
# STEP 6: DEFINE ORIGIN (RELEASE vs RESEARCH SPACE)
# =========================================================

def classify_origin(path: str):
    path = str(path)
    if "research-lettuceknow-releases/" in path:
        return "R"   # Release space
    elif "research-lettuceknow/" in path:
        return "RS"  # Research space
    else:
        return "OTHER"

df_ALD_v1["ORIGIN"] = df_ALD_v1["COLL_NAME"].apply(classify_origin)


# =========================================================
# STEP 7: EXTRACT END NAME (FILE OR LAST DIRECTORY)
# =========================================================

df_ALD_v1["END_NAME"] = df_ALD_v1["COLL_NAME"].apply(
    lambda x: Path(str(x)).name
)

# =========================================================
# STEP 8: LABEL RELEASE VERSION (V1 / V2 / NONE)
# =========================================================

def classify_release(path: str):
    path = str(path)
    if "data-release_V1_" in path:
        return "V1"
    elif "data-release_V2_" in path:
        return "V2"
    else:
        return None

df_ALD_v1["RELEASE_VERSION"] = df_ALD_v1["COLL_NAME"].apply(classify_release)


# =========================================================
# STEP 9: BUILD CROSS-SPACE PRESENCE TABLE
# =========================================================

# Key idea:
# We check whether the SAME END_NAME exists in release space
# for the same ALD.

release_set = set(
    df_ALD_v1[df_ALD_v1["ORIGIN"] == "R"]
    .apply(lambda r: (r["ALD_id"], r["END_NAME"]), axis=1)
)

research_set = set(
    df_ALD_v1[df_ALD_v1["ORIGIN"] == "RS"]
    .apply(lambda r: (r["ALD_id"], r["END_NAME"]), axis=1)
)


def check_in_release(row):
    return (row["ALD_id"], row["END_NAME"]) in release_set


def check_in_research(row):
    return (row["ALD_id"], row["END_NAME"]) in research_set


df_ALD_v1["IN_RELEASE"] = df_ALD_v1.apply(check_in_release, axis=1)
df_ALD_v1["IN_RESEARCH"] = df_ALD_v1.apply(check_in_research, axis=1)


# =========================================================
# STEP 10: SAFE DELETION RULE (VERY CONSERVATIVE)
# =========================================================

# You ONLY delete if:
# - file is in research space
# - AND exact match exists in release space

df_ALD_v1["SAFE_DELETE_RESEARCH"] = (
    (df_ALD_v1["ORIGIN"] == "RS") &
    (df_ALD_v1["IN_RELEASE"] == True)
)

# Everything else is NOT safe
df_ALD_v1["SAFE_STATUS"] = "KEEP"

df_ALD_v1.loc[
    df_ALD_v1["SAFE_DELETE_RESEARCH"],
    "SAFE_STATUS"
] = "DELETE_CANDIDATE"


# =========================================================
# STEP 11: SANITY CHECK SUMMARY
# =========================================================

print("\n===== SAFE DELETION SUMMARY =====")
print(df_ALD_v1["SAFE_STATUS"].value_counts())

print("\n===== ORIGIN DISTRIBUTION =====")
print(df_ALD_v1["ORIGIN"].value_counts())

print("\n===== RELEASE COVERAGE =====")
print(df_ALD_v1.groupby(["RELEASE_VERSION", "ORIGIN"]).size())


# =========================================================
# STEP 12: EXPORT AUDIT TABLE
# =========================================================

out_file = "/home/melanie/Documents/LK_data/LK_inventory_report/11_RNAseq_delete_table.csv"

df_ALD_v1.sort_values(["ALD_id", "END_NAME"]).to_csv(out_file, index=False)

print(f"\nAudit table saved to: {out_file}")

# =========================================================
# STEP 13: FILTER ONLY SAFE DELETE CANDIDATES (RESEARCH SPACE)
# =========================================================

to_delete_df = df_ALD_v1[
    df_ALD_v1["SAFE_STATUS"] == "DELETE_CANDIDATE"
].copy()

print(f"\nSafe delete candidates: {len(to_delete_df)} rows")


# =========================================================
# STEP 14: CLASSIFY SUB-DIRECTORY (processed / raw / other)
# =========================================================

def classify_subdir(path: str):
    path = str(path)
    if "/processed_data/" in path:
        return "processed_data"
    elif "/raw_data/" in path:
        return "raw_data"
    else:
        return "other"

to_delete_df["SUBDIR_TYPE"] = to_delete_df["COLL_NAME"].apply(classify_subdir)


# =========================================================
# STEP 15 DEBUG EXPORT: INSPECT ALD PARENT EXTRACTION
# =========================================================

debug_ald_parent = to_delete_df[
    ["ALD_id", "COLL_NAME", "ALD_PARENT_DIR"]
].copy()

debug_file = Path(
    "/home/melanie/Documents/LK_data/LK_inventory_report/debug_ALD_PARENT_DIR.csv"
)

# sample both head + random spread for safety inspection
sample_df = pd.concat([
    debug_ald_parent.head(500),
    debug_ald_parent.sample(500, random_state=42)
])

sample_df.to_csv(debug_file, index=False)

print(f"\nSaved ALD parent debug file to:\n{debug_file}")

breakpoint()

# =========================================================
# STEP 16: LOAD L5 COLLECTION INVENTORY
# =========================================================

l5_file = Path(
    "/home/melanie/Documents/LK_data/LK_inventory_report/merged_inventory_L5.csv"
)

l5_df = pd.read_csv(l5_file)

print(f"Loaded L5 collection inventory: {len(l5_df)} rows")

l5_df["collection"] = l5_df["collection"].astype(str)

l5_df["collection_size_bytes"] = pd.to_numeric(
    l5_df["collection_size_bytes"],
    errors="coerce"
).fillna(0)


# =========================================================
# STEP 16.5: NORMALISE PATHS (CRITICAL FIX)
# =========================================================

def normalize_path(p):
    p = str(p)
    p = p.replace("/nluu6p/home/", "")
    return p


to_delete_df["COLL_NORM"] = to_delete_df["COLL_NAME"].apply(normalize_path)
l5_df["collection_norm"] = l5_df["collection"].apply(normalize_path)

# =========================================================
# STEP 17: FAST PREFIX MATCH (FIXED)
# =========================================================

l5_df = l5_df.sort_values(
    "collection_norm",
    key=lambda x: x.str.len(),
    ascending=False
)

collections = l5_df["collection_norm"].to_numpy()

def match_l5(path):
    path = str(path)
    for c in collections:
        if path.startswith(c):
            return c
    return None


to_delete_df["L5_COLLECTION"] = to_delete_df["COLL_NORM"].map(match_l5)

print(
    "Mapped:",
    to_delete_df["L5_COLLECTION"].notna().sum(),
    "/",
    len(to_delete_df)
)

breakpoint()


# =========================================================
# STEP 18: ADD CORRECT SIZE FROM L5 INVENTORY
# =========================================================

to_delete_df = to_delete_df.merge(
    l5_df[["collection_norm", "collection_size_bytes"]],
    left_on="L5_COLLECTION",
    right_on="collection_norm",
    how="left"
)

to_delete_df["collection_size_bytes"] = (
    to_delete_df["collection_size_bytes"].fillna(0)
)

breakpoint()


# =========================================================
# STEP 19: ORIGIN CLASSIFICATION
# =========================================================

def classify_origin(path: str):
    path = str(path)
    if "/research-lettuceknow-releases/" in path:
        return "release"
    elif "/research-lettuceknow/" in path:
        return "research"
    else:
        return "other"

to_delete_df["ORIGIN"] = to_delete_df["COLL_NAME"].apply(classify_origin)

breakpoint()


# =========================================================
# STEP 20: EXTRACT ALD PARENT DIRECTORY
# =========================================================

def extract_ald_parent(path: str):
    parts = Path(str(path)).parts
    for i, p in enumerate(parts):
        if p.startswith("ALD"):
            return "/".join(parts[:i+1])
    return None

to_delete_df["ALD_PARENT_DIR"] = to_delete_df["COLL_NAME"].apply(extract_ald_parent)

breakpoint()


# =========================================================
# STEP 21: FINAL SUMMARY
# =========================================================

summary_delete = to_delete_df.groupby(
    ["ALD_id", "ALD_PARENT_DIR", "ORIGIN", "L5_COLLECTION"]
).agg(
    num_files=("COLL_NAME", "count"),
    total_size_bytes=("collection_size_bytes", "sum")
).reset_index()

summary_delete["total_size_GB"] = summary_delete["total_size_bytes"] / 1e9
summary_delete["total_size_TB"] = summary_delete["total_size_bytes"] / 1e12

breakpoint()


# =========================================================
# STEP 22: DELETE SAFETY FLAG
# =========================================================

summary_delete["SAFE_TO_DELETE"] = summary_delete["ORIGIN"].apply(
    lambda x: True if x == "research" else False
)


# =========================================================
# STEP 23: SORT BY IMPACT
# =========================================================

summary_delete = summary_delete.sort_values(
    by=["total_size_bytes", "num_files"],
    ascending=False
)


# =========================================================
# STEP 24: EXPORT FINAL TABLE
# =========================================================

out_file = Path(
    "/home/melanie/Documents/LK_data/LK_inventory_report/11_safe_delete_summary_corrected.csv"
)

summary_delete.to_csv(out_file, index=False)

print(f"Saved corrected summary: {out_file}")
print(summary_delete.head())



breakpoint()

# =========================================================
# STEP 16: LOAD L5 COLLECTION INVENTORY
# =========================================================

l5_file = Path(
    "/home/melanie/Documents/LK_data/LK_inventory_report/merged_inventory_L5.csv"
)

l5_df = pd.read_csv(l5_file)

print(f"Loaded L5 collection inventory: {len(l5_df)} rows")

# IMPORTANT: column is "collection", not COLL_NAME
l5_df["collection"] = l5_df["collection"].astype(str)

# ensure numeric
l5_df["collection_size_bytes"] = pd.to_numeric(
    l5_df["collection_size_bytes"],
    errors="coerce"
).fillna(0)


# =========================================================
# STEP 17: FAST PREFIX MATCH
# =========================================================

# sort collections so deepest match comes first
l5_df = l5_df.sort_values(
    "collection",
    key=lambda x: x.str.len(),
    ascending=False
)

collections = l5_df["collection"].to_numpy()

def match_l5(path):
    path = str(path)
    for c in collections:
        if path.startswith(c):
            return c
    return None


# apply ONCE only (no inner apply!)
to_delete_df["L5_COLLECTION"] = to_delete_df["COLL_NAME"].map(match_l5)

print(
    "Mapped:",
    to_delete_df["L5_COLLECTION"].notna().sum(),
    "/",
    len(to_delete_df)
)

breakpoint()

# =========================================================
# STEP 18: ADD CORRECT SIZE FROM L5 INVENTORY
# =========================================================

to_delete_df = to_delete_df.merge(
    l5_df[["collection", "collection_size_bytes"]],
    left_on="L5_COLLECTION",
    right_on="collection",
    how="left"
)

to_delete_df["collection_size_bytes"] = to_delete_df["collection_size_bytes"].fillna(0)

breakpoint()

# =========================================================
# STEP 19: ORIGIN CLASSIFICATION
# =========================================================

def classify_origin(path: str):
    path = str(path)
    if "/research-lettuceknow-releases/" in path:
        return "release"
    elif "/research-lettuceknow/" in path:
        return "research"
    else:
        return "other"

to_delete_df["ORIGIN"] = to_delete_df["COLL_NAME"].apply(classify_origin)

breakpoint()

# =========================================================
# STEP 20: EXTRACT ALD PARENT DIRECTORY (KEEP YOUR STEP 15 LOGIC)
# =========================================================

def extract_ald_parent(path: str):
    parts = Path(str(path)).parts
    for i, p in enumerate(parts):
        if p.startswith("ALD"):
            return "/".join(parts[:i+1])
    return None

to_delete_df["ALD_PARENT_DIR"] = to_delete_df["COLL_NAME"].apply(extract_ald_parent)

breakpoint()

# =========================================================
# STEP 21: FINAL SUMMARY (CORRECT SIZE SOURCE)
# =========================================================

summary_delete = to_delete_df.groupby(
    ["ALD_id", "ALD_PARENT_DIR", "ORIGIN", "L5_COLLECTION"]
).agg(
    num_files=("COLL_NAME", "count"),
    total_size_bytes=("collection_size_bytes", "sum")
).reset_index()


summary_delete["total_size_GB"] = summary_delete["total_size_bytes"] / 1e9
summary_delete["total_size_TB"] = summary_delete["total_size_bytes"] / 1e12

breakpoint()

# =========================================================
# STEP 22: DELETE SAFETY FLAG
# =========================================================

summary_delete["SAFE_TO_DELETE"] = summary_delete["ORIGIN"].apply(
    lambda x: True if x == "research" else False
)


# =========================================================
# STEP 23: SORT BY IMPACT
# =========================================================

summary_delete = summary_delete.sort_values(
    by=["total_size_bytes", "num_files"],
    ascending=False
)


# =========================================================
# STEP 24: EXPORT FINAL TABLE
# =========================================================

out_file = Path(
    "/home/melanie/Documents/LK_data/LK_inventory_report/11_safe_delete_summary_corrected.csv"
)

summary_delete.to_csv(out_file, index=False)

print(f"Saved corrected summary: {out_file}")
print(summary_delete.head())