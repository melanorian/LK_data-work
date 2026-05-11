#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------- CONFIGURATION ----------------
base_dir = Path("/home/melanie/Documents/LK_data/LK_inventory_report")

input_file = base_dir / "9_summarized_inventory_classified_L5.csv"

out_dir = base_dir / "visualisation"
out_dir.mkdir(parents=True, exist_ok=True)
# ----------------------------------------------


# ---------------- LOAD DATA ----------------
df = pd.read_csv(input_file)

df["released"] = df["released"].fillna(0).astype(int)
df["release_version"] = df["release_version"].fillna("unknown")
df["data_domain"] = df["data_domain"].fillna("unknown")
df["processing_level"] = df["processing_level"].fillna("unknown")


# =========================================================
# 1. PIE: release status
# =========================================================
df_release = df.copy()

df_release["release_group"] = df_release.apply(
    lambda r: "Not released" if r["released"] == 0
    else ("DR1" if r["release_version"] == "DR1"
          else ("DR2" if r["release_version"] == "DR2"
                else "Other")),
    axis=1
)

release_sum = df_release.groupby("release_group")["collection_size_bytes"].sum()

plt.figure()
plt.pie(release_sum, labels=release_sum.index, autopct="%1.1f%%")
plt.title("Storage by release status")
plt.savefig(out_dir / "pie_release_status.svg")
plt.close()


# =========================================================
# 2. PIE: data domain
# =========================================================
domain_sum = df.groupby("data_domain")["collection_size_bytes"].sum()

plt.figure()
plt.pie(domain_sum, labels=domain_sum.index, autopct="%1.1f%%")
plt.title("Storage by data domain")
plt.savefig(out_dir / "pie_domain_all.svg")
plt.close()


# =========================================================
# 3. PIE: processing level
# =========================================================
proc_sum = df.groupby("processing_level")["collection_size_bytes"].sum()

plt.figure()
plt.pie(proc_sum, labels=proc_sum.index, autopct="%1.1f%%")
plt.title("Storage by processing level")
plt.savefig(out_dir / "pie_processing_level.svg")
plt.close()


# =========================================================
# 4. STACKED BAR: processing level per domain
# =========================================================
bar_df = df.groupby(["data_domain", "processing_level"])["collection_size_bytes"].sum().unstack(fill_value=0)

bar_df.plot(kind="bar", stacked=True, figsize=(10,6))

plt.title("Processing level per data domain")
plt.xlabel("Data domain")
plt.ylabel("Size (bytes)")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig(out_dir / "stacked_processing_by_domain.svg")
plt.close()