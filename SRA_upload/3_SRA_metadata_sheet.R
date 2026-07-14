# SRA Submission Prep Script — batch version
# Basic set-up
rm(list = ls())

# ---- Load libraries -----------------------------------------
library(dplyr)
library(tidyr)
library(readr)
library(stringr)
library(openxlsx)

# ---- 1. PATHS -----------------------------------------------
in_dir       <- "~/Documents/LK_data/RNAseq/Metadata_sheets_SRA/1_Metadata_pre-processing/"
sra_template <- "~/Documents/LK_data/RNAseq/Templates/SRA_metadata_templates.xlsx"
out_dir      <- "~/Documents/LK_data/RNAseq/Metadata_sheets_SRA/3_SRA_metadata/"

# Create output directory if it doesn't exist
if (!dir.exists(out_dir)) {
  dir.create(out_dir, recursive = TRUE)
  cat("Created output directory:", out_dir, "\n")
}

# Read CSV files
# Read CSV files 
csv_files <- list.files(in_dir, pattern = "\\.csv$", full.names = FALSE)


csv_list <- list()

for (csv_file in csv_files) {
  
  exp_name <- str_remove(csv_file, "\\.csv$")
  cat("Processing:", exp_name, "\n")
  
  # Load & filter I1/I2 index reads 
  meta <- read_csv(paste0(in_dir, csv_file), show_col_types = FALSE)
  
  meta_filtered <- meta %>%
    filter(!str_detect(basename(name_no_ext), "_(I1|I2)_"))
  
  csv_list[[exp_name]] <- as.data.frame(meta_filtered)
  
}

# 2. Extract file-wise key information

meta_list <- list()

for (csv_file in csv_files) {

  exp_name <- str_remove(csv_file, "\\.csv$")
  cat("Processing:", exp_name, "\n")

  # -- Load & filter I1/I2 index reads ------------------------
  meta <- read_csv(paste0(in_dir, csv_file), show_col_types = FALSE)

  meta_filtered <- meta %>%
    filter(!str_detect(basename(name_no_ext), "_(I1|I2)_"))

  # -- Build file path data frame and store in list -----------
  meta_list[[exp_name]] <- data.frame(
    sample_name = meta_filtered$SampleID_submission.x,
    library_ID  = meta_filtered$name_no_ext,
    full_name   = meta_filtered$full_name,
    file_path   = meta_filtered$file_path, 
    sra_submission = meta_filtered$SRA_submission_unique
  )
}

cat("Done! Processed", length(csv_files), "files.\n")

# Add _add-seq suffix to library_ID where file_path contains additional sequencing substring (to have unique library_IDs)
add_seq_suffix <- function(df) {
  df %>%
    mutate(library_ID = ifelse(
      str_detect(file_path, "additional.sequencing"),  # matches additional-sequencing, additional_sequencing etc.
      paste0(library_ID, "_add-seq"),
      library_ID
    ))
}

# Apply to all experiments in meta_list
meta_list <- lapply(meta_list, add_seq_suffix)

# ---- split into R1 and R2 data frames ----------

rsplit_r1_r2 <- function(sra_df) {

  r1 <- sra_df %>%
    filter(str_detect(library_ID, "_R1_")) %>%
    mutate(
      pair_key  = str_remove(library_ID, "_R1_.*$"),
      filename1 = full_name
    )
  
  r2 <- sra_df %>%
    filter(str_detect(library_ID, "_R2_")) %>%
    mutate(
      pair_key  = str_remove(library_ID, "_R2_.*$"),
      filename1 = full_name
    )

  r3 <- cbind(r1, r2)
  colnames(r3) <- c("sample_name", "library_ID", "filename1", "file_path1", "pair_key", "library_ID_R1",
                    "sample_name2", "library_ID2", "filename2", "file_path2", "pair_key2", "library_ID_R2")
  r3 <- r3 %>%
    select(sample_name, library_ID, filename1, file_path1, filename2, file_path2)
}

# Build SRA df 
build_sra_df <- function(sra_df, csv_list_element) {
  
  # Look up Other_sampleID.x from full metadata using file_path1 as key
  other_id_lookup <- csv_list_element %>%
    select(file_path, Other_sampleID.x, Sequencing_platform) %>%
    distinct()
  
  # Helper to ensure filename ends in .fastq.gz
  fix_extension <- function(x) {
    case_when(
      is.na(x)                  ~ NA_character_,
      str_detect(x, "\\.tar$")  ~ str_replace(x, "\\.tar$", ".fastq.gz"),
      str_detect(x, "\\.fastq\\.gz$") ~ x,
      TRUE                      ~ paste0(x, ".fastq.gz")
    )
  }
  
  sra_df %>%
    left_join(other_id_lookup, by = c("file_path1" = "file_path")) %>%
    transmute(
      sample_name        = sample_name,
      library_ID         = str_replace(library_ID, "_R1_.*?(_add-seq)?$", "\\1"),
      title              = paste0("RNA-seq", " ", Other_sampleID.x),
      library_strategy   = "ssRNA-seq",
      library_source     = "TRANSCRIPTOMIC",
      library_selection  = "PolyA",
      library_layout     = "paired",         # ADJUST MANUALLY
      platform           = "ILLUMINA",       # ADJUST MANUALLY
      instrument_model   = Sequencing_platform,
      design_description = "NA",
      filetype           = "fastq",
      filename           = fix_extension(filename1),
      filename2          = fix_extension(filename2),
      filename3          = NA,
      filename4          = NA,
      assembly           = NA,
      fasta_file         = NA
    )
}

# Apply per experiment
sra_results <- list()
for (exp_name in names(meta_list)) {
  paired   <- rsplit_r1_r2(meta_list[[exp_name]])
  sra_results[[exp_name]] <- build_sra_df(paired, csv_list[[exp_name]])
}

for (exp_name in names(sra_results)) {
  
  wb_sra <- loadWorkbook(sra_template)
  sheet_name <- sheets(wb_sra)[2]
  
  writeData(wb_sra,
            sheet    = sheet_name,
            x        = sra_results[[exp_name]],
            startRow = 2,
            startCol = 1,
            colNames = FALSE)
  
  saveWorkbook(wb_sra,
               file      = paste0(out_dir, exp_name, "_SRA_metadata.xlsx"),
               overwrite = TRUE)
  
  cat("Saved:", paste0(exp_name, "_SRA_metadata.xlsx"), "\n")
}

# Save meta_list elements as csv
for (exp_name in names(meta_list)) {
  
  write_csv(meta_list[[exp_name]],
            file = paste0(out_dir, exp_name, "_SRA_paths.csv"))
  
  cat("Saved:", paste0(exp_name, "_SRA_paths.csv"),
      "—", nrow(meta_list[[exp_name]]), "rows\n")
}


### CHECK

library(readxl)
release_grouping_file <- "~/Documents/LK_data/RNAseq/YODA_Metadata_files/20260617_suggested_RNAseq_groups_SRA_submission.xlsx"
grouping <- excel_sheets(release_grouping_file)

exp_grouping <- setNames(
  lapply(names(csv_list), function(sh) {
    read_excel(release_grouping_file, sheet = sh)
  }),
  names(csv_list)
)

# For all experiments: find missing samples and save as csv
for (exp_name in names(exp_grouping)) {
  
  # Get SampleIDs in grouping file not found in sra_results
  missing <- unique(exp_grouping[[exp_name]]$SampleID_submission)[
    !unique(exp_grouping[[exp_name]]$SampleID_submission) %in% unique(sra_results[[exp_name]]$sample_name)
  ]
  
  # Extract missing rows from grouping
  missing_gr <- exp_grouping[[exp_name]] %>%
    filter(SampleID_submission %in% missing)
  
  cat(exp_name, "— missing:", length(missing), "samples\n")
  
  # Save only if there are missing samples
  if (nrow(missing_gr) > 0) {
    write_csv(missing_gr,
              file = paste0(out_dir, exp_name, "_missing_samples.csv"))
    cat("  Saved:", paste0(exp_name, "_missing_samples.csv"), "\n")
  }
}


### Additional processing if needed

## ExpMA011

csv_11 <- csv_list$ExpMA011
exp_group_11 <- exp_grouping$ExpMA011
meta_list_11 <- meta_list$ExpMA011
