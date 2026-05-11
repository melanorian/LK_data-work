#!/usr/bin/env python

import pandas as pd
from pathlib import Path
import json

# ----------------- CONFIGURATION -----------------
BASE_DIR = Path("/home/melanie/Documents/LK_data/LK_inventory_report")
MAX_LEVEL = 5

# Input file
SUMMARY_FILE = BASE_DIR / f"8_summarized_inventory_with_duplicates_L{MAX_LEVEL}.csv"

# Output file
OUT_FILE = BASE_DIR / f"9_summarized_inventory_classified_L{MAX_LEVEL}.csv"
# ---------------------------------------------------


# Step 1: LOAD DATA
df = pd.read_csv(SUMMARY_FILE)

print(f"Loaded {len(df)} collections")


# Step 2: DEFINE CLASSIFICATION FUNCTIONS

def load_file_types(file_types):

    try:
        return json.loads(file_types) if pd.notna(file_types) else {}
    except:
        return {}


def classify_processing_level(collection, file_types):
    """
    Classify collection processing stage
    """

    c = str(collection).lower()
    ft = load_file_types(file_types)
    ft_keys = set(ft.keys())

    image_types = {
        "jpg", "jpeg", "png",
        "tif", "tiff", "ply",
        "JPG"
    }

    processed_types = {
        "bam", "bai",
        "cram", "crai",
        "sam",
        "vcf", "vcf.gz",
        "tbi",
        "csv", "tsv",
        "xls", "xlsx",
        "pdf",
        "html"
    }

    # RELEASE DATA
    if c.startswith("research-lettuceknow-releases/"):
        return "release_data"

    # RAW DATA
    if (
        "raw_data" in c
        or "raw-data" in c
        or "acquisition" in c
        or len(ft_keys.intersection(image_types)) > 0
    ):
        return "raw_data"

    # RESULTS
    if (
        "/results/" in c
        or c.startswith("research-lettuceknow/results/")
    ):
        return "results_data"

    # PROCESSED DATA
    if (
        "processed_data" in c
        or "processed-data" in c
        or "processed" in c
        or "variant" in c
        or "mapping" in c
        or len(ft_keys.intersection(processed_types)) > 0
    ):
        return "processed_data"

    return "mixed_or_unknown"


def classify_domain(collection, file_types):
    """
    Broad scientific domain classification
    """

    c = str(collection).lower()
    ft = load_file_types(file_types)
    ft_keys = set(ft.keys())

    image_types = {
        "jpg", "jpeg", "png",
        "tif", "tiff", "ply",
        "JPG"
    }

    # RNA / transcriptomics
    if (
        "rna" in c
        or "rnaseq" in c
        or "transcript" in c
    ):
        return "RNA"

    # DNA / genomics
    if (
        "dna" in c
        or "variant" in c
        or "vcf" in c
        or "gvcf" in c
    ):
        return "DNA"

    # Phenotyping / imaging
    if (
        "field" in c
        or "phenotyping" in c
        or "image" in c
        or "images" in c
        or "imaging" in c
        or "camera" in c
        or "acquisition" in c
        or len(ft_keys.intersection(image_types)) > 0
    ):
        return "phenotyping"

    return "unknown"


def classify_special_cases(collection):
    """
    Identify transfer tests, third-party data etc.
    """

    c = str(collection).lower()

    if "transfer_test" in c or "transfer_tests" in c:
        return "transfer_test"

    if "3rd_party" in c or "third_party" in c:
        return "third_party_data"

    if "_todelete" in c or "to_delete" in c:
        return "marked_for_deletion"

    return ""


def classify_release(collection):
    """
    Determine release status/version
    """

    c = str(collection)

    if c.startswith("research-lettuceknow-releases/"):

        if "data-release_V1" in c:
            return pd.Series([1, "DR1"])

        if "data-release_V2" in c:
            return pd.Series([1, "DR2"])

        return pd.Series([1, "unknown_release"])

    return pd.Series([0, ""])


# Step 3: APPLY CLASSIFICATIONS

df["processing_level"] = df.apply(
    lambda row: classify_processing_level(
        row["collection"],
        row.get("file_types", "")
    ),
    axis=1
)

df["data_domain"] = df.apply(
    lambda row: classify_domain(
        row["collection"],
        row.get("file_types", "")
    ),
    axis=1
)

df["special_category"] = df["collection"].apply(
    classify_special_cases
)

df[["released", "release_version"]] = df["collection"].apply(
    classify_release
)


# Step 4: QUICK OVERVIEW

print("\nProcessing level overview:")
print(df["processing_level"].value_counts())

print("\nDomain overview:")
print(df["data_domain"].value_counts())

print("\nSpecial categories overview:")
print(df["special_category"].value_counts())

print("\nRelease overview:")
print(df["release_version"].value_counts())


# Step 5: SAVE OUTPUT

df.to_csv(OUT_FILE, index=False)

print(f"\nSaved classified inventory to:")
print(OUT_FILE)