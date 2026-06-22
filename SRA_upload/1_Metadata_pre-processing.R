# Basic set-up
rm(list = ls())

## Load Libraries
library(readxl)
library(readr)
library(dplyr)
library(purrr)
library(stringr)

## Set working directory to location with metadata
wd <- "~/Documents/LK_data/RNAseq/YODA_Metadata_files"
setwd(wd)

# Load Files

## Define file content
metadata_master_file <- "seq_metadata_all_releases_V9_20250821.tsv"
release_grouping_file <- "20260617_suggested_RNAseq_groups_SRA_submission.xlsx"
raw_location_file <- "10_paths-to-all-raw-seq-data.tsv"   

## Load files
meta_master <- read_tsv(metadata_master_file)
grouping <- excel_sheets(release_grouping_file)
raw_location <- read_tsv(raw_location_file)

exp_tabs <- c(
  "ExpAH001",
  "ExpMA002",
  "ExpMA003",
  "ExpMA011",
  "ExpMA012",
  "ExpMA013",
  "ExpMA015",
  "ExpMA016",
  "LKAtlasRNAseq001",
  "LKAtlasRNAseq002",
  "LKAtlasRNAseq003",
  "LKAtlasRNAseq004"
)

exp_grouping <- setNames(
  lapply(exp_tabs, function(sh) {
    read_excel(release_grouping_file, sheet = sh)
  }),
  exp_tabs
)

# Build a table that contains only essential sample information/submission

# columns expected
expected_cols <- c(
  "Unique_SampleID_in_metadata",
  "SampleID_submission",
  "Other_sampleID",
  "expID_plant",
  "SRA_submission",
  "SRA_submission_unique",
  "on_SRA",
  "SRA_ID"
)

# check each sheet
col_check <- lapply(names(exp_grouping), function(sh) {
  
  df <- exp_grouping[[sh]]
  
  data.frame(
    sheet = sh,
    missing_cols = paste(setdiff(expected_cols, names(df)), collapse = ", "),
    n_cols = length(names(df))
  )
})

col_check <- bind_rows(col_check)

# show only sheets with missing columns
col_check %>%
  filter(missing_cols != "")


# create table with sample groups
sample_groups <- lapply(names(exp_grouping), function(sh) {
  
  df <- exp_grouping[[sh]]
  
  df %>%
    mutate(exp_tab = sh) %>%
    select(any_of(c(expected_cols, "exp_tab")))
})

clean_on_sra <- function(x) {
  case_when(
    x %in% c(TRUE, "TRUE", "T", "t", 1, "1", "yes", "YES") ~ TRUE,
    x %in% c(FALSE, "FALSE", "F", "f", 0, "0", "no", "NO") ~ FALSE,
    TRUE ~ NA
  )
}

sample_groups <- lapply(names(exp_grouping), function(sh) {
  
  df <- exp_grouping[[sh]]
  
  # force column types BEFORE selecting
  if ("on_SRA" %in% names(df)) {
    df$on_SRA <- clean_on_sra(df$on_SRA)
  }
  
  df %>%
    mutate(exp_tab = sh) %>%
    select(any_of(c(expected_cols, "exp_tab")))
})

sample_groups <- bind_rows(sample_groups)
#write.csv(sample_groups, paste0(wd, "/", "sample_grouping_long.csv"))

# Create a file with merged information 
## A) merge metadata with grouping
meta_master_SRA <- meta_master %>%
  left_join(sample_groups, by = "Unique_SampleID_in_metadata")

## B) merge with file location
## B1 Extract substring from file path to match with sample submission ID

raw_location2 <- raw_location %>%
  mutate(
    # 1. get filename only
    full_name = basename(file_path),
    # 2. remove known extensions (.fastq.gz OR .tar OR other single extensions)
    name_no_ext = str_remove(full_name, "\\.fastq\\.gz$|\\.tar$|\\.[^.]+$"),
    # 3. extract sample core = before first underscore
    sample_core = str_extract(name_no_ext, "^[^_]+")
  )

# Add column to indicate match of extracted sample name in meta_master_SRA
meta_master_SRA <- meta_master_SRA %>%
  mutate(
    SampleID_submission_match_file_path =
      SampleID_submission.x %in% raw_location2$sample_core
  )

table(meta_master_SRA$SampleID_submission_match_file_path, useNA = "ifany")


############## CONSTRUCTION STARTS ####################################

# Join
meta_master_SRA_long <- meta_master_SRA %>%
  left_join(
    raw_location2,
    by = c("SampleID_submission.x" = "sample_core"),
    relationship = "many-to-many"
  )



############## CONSTRUCTION ENDS ####################################


# sanity check

meta_master_SRA_long <- meta_master_SRA_long %>%
  mutate(
    folder_from_path = str_extract(file_path, "(?<=/)ALD[^/]+(?=/)"),
    
    check_FolderID = folder_from_path == Seqdata_FolderID
  )

meta_master_SRA_long <- meta_master_SRA_long %>%
  mutate(
    folder_from_path = str_match(file_path, ".*/([^/]+)/[^/]+$")[,2],
    check_FolderID = folder_from_path == Seqdata_FolderID
  )

folder_check_summary <- meta_master_SRA_long %>%
  summarise(
    TRUE_count = sum(check_FolderID, na.rm = TRUE),
    FALSE_count = sum(!check_FolderID, na.rm = TRUE),
    NA_count = sum(is.na(check_FolderID))
  )

folder_check_summary

meta_master_SRA_long_TRUE <- meta_master_SRA_long %>%
  filter(check_FolderID == TRUE)

meta_master_SRA_long_FALSE <- meta_master_SRA_long %>%
  filter(check_FolderID == FALSE)

meta_master_SRA_long_NA <- meta_master_SRA_long %>%
  filter(is.na(check_FolderID))

#### CHECK OUTPUT if correct continue

# Split into individual overview sheets/submission package

# 1. Filter for specific experiment ID expID_plant.y == exp_tabs
# 2. Filter for on_SRA == FALSE
# 3. Check for nrow of resulting df. If ==0 print exp_tabs selection length is zero , If >0 proceed with 4.
# 4. create df of the selection
# 5. ensure the name of the data frame is the matching exp_tabs element

# Create one data frame per experiment containing only samples not yet on SRA
experiment_dfs <- lapply(exp_tabs, function(exp_id) {
  # Filter for current experiment and samples not yet submitted
  df <- meta_master_SRA_long %>%
    filter(
      expID_plant.y == exp_id,
      on_SRA == FALSE
    )
  # Check if any rows were found
  if (nrow(df) == 0) {
    message(exp_id, ": selection length is zero")
    return(NULL)
  } else {
    message(exp_id, ": ", nrow(df), " rows selected")
    return(df)
  }
})

# Assign experiment names to list elements
names(experiment_dfs) <- exp_tabs
# Remove empty entries
experiment_dfs <- experiment_dfs[!sapply(experiment_dfs, is.null)]
# Create individual data frames in the global environment
list2env(experiment_dfs, envir = .GlobalEnv)

# safe overview output for manual inspection
output_dir <- file.path("~/Documents/LK_data/RNAseq/Metadata_sheets_SRA/", "1_Metadata_pre-processing")
dir.create(output_dir, showWarnings = FALSE)

lapply(names(experiment_dfs), function(exp_id) {
  
  df <- experiment_dfs[[exp_id]]
  
  write.csv(
    df,
    file = file.path(output_dir, paste0(exp_id, ".csv")),
    row.names = FALSE
  )
})


sum(unique(ExpMA016$Unique_SampleID_in_metadata) == unique(meta_master$Unique_SampleID_in_metadata[meta_master$expID_RNA == "ExpMA016"]))


