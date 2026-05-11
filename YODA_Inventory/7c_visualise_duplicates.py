#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------- CONFIGURATION ----------------

BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

INPUT_FILE = BASE_DIR / "7b_delete_duplicates.csv"

OUT_DIR = BASE_DIR / "visualisation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE_DELETE = OUT_DIR / "7c_pie_delete_duplicates.svg"
OUT_FILE_TIER = OUT_DIR / "7c_pie_delete_duplicates_by_tier.svg"

# ------------------------------------------------


# ---------------- LOAD DATA ----------------

df = pd.read_csv(INPUT_FILE)

# ensure boolean
df["delete_duplicate"] = df["delete_duplicate"].astype(bool)

# ensure numeric
df["DATA_SIZE"] = pd.to_numeric(
    df["DATA_SIZE"],
    errors="coerce"
).fillna(0)

# ------------------------------------------------
# PIE 1 — DELETE VS KEEP
# ------------------------------------------------

summary = (
    df.groupby("delete_duplicate")["DATA_SIZE"]
    .sum()
    .reset_index()
)

summary["TB"] = summary["DATA_SIZE"] / 1e12

summary["label"] = summary.apply(
    lambda row:
    f"Delete candidates ({round(row['TB'])} TB)"
    if row["delete_duplicate"]
    else f"Keep ({round(row['TB'])} TB)",
    axis=1
)

fig1, ax1 = plt.subplots(figsize=(8, 8))

ax1.pie(
    summary["DATA_SIZE"],
    labels=summary["label"],
    autopct="%1.1f%%"
)

ax1.set_title("Potentially deletable duplicate data")

plt.savefig(
    OUT_FILE_DELETE,
    format="svg",
    bbox_inches="tight"
)

plt.close(fig1)

# ------------------------------------------------
# STORAGE TIER LABELS
# ------------------------------------------------

def classify_storage_tier(path):

    path = str(path)

    if "data-release_V2" in path:
        return "research-lettuceknow-release_V2"

    elif "data-release_V1" in path:
        return "research-lettuceknow-release_V1"

    else:
        return "research-lettuceknow"

df["storage_tier"] = df["file_path"].apply(classify_storage_tier)

# ------------------------------------------------
# PIE 2 — DELETABLE DATA PER STORAGE TIER
# ------------------------------------------------

delete_df = df[df["delete_duplicate"] == True].copy()

tier_summary = (
    delete_df.groupby("storage_tier")["DATA_SIZE"]
    .sum()
    .reset_index()
)

tier_summary["TB"] = tier_summary["DATA_SIZE"] / 1e12

tier_summary["label"] = tier_summary.apply(
    lambda row:
    f"{row['storage_tier']} ({round(row['TB'])} TB)",
    axis=1
)

fig2, ax2 = plt.subplots(figsize=(8, 8))

ax2.pie(
    tier_summary["DATA_SIZE"],
    labels=tier_summary["label"],
    autopct="%1.1f%%"
)

ax2.set_title("Deletable duplicate data by storage tier")

plt.savefig(
    OUT_FILE_TIER,
    format="svg",
    bbox_inches="tight"
)

plt.close(fig2)

# ------------------------------------------------
# DONE
# ------------------------------------------------

print(f"Saved: {OUT_FILE_DELETE}")
print(f"Saved: {OUT_FILE_TIER}")