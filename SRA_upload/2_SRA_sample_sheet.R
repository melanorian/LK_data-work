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
sra_template <- "~/Documents/LK_data/RNAseq/Templates/SRA_Sample_template.xlsx"
out_dir      <- "~/Documents/LK_data/RNAseq/Metadata_sheets_SRA/2_SRA_samples/"

# Create output directory if it doesn't exist
if (!dir.exists(out_dir)) {
  dir.create(out_dir, recursive = TRUE)
  cat("Created output directory:", out_dir, "\n")
}

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

#csv_list <- csv_list$ExpMA002

# Build SRA df 
# Build BioSample attribute sheet
build_biosample_df <- function(csv_list_element) {
  
  csv_list_element %>%
    distinct(SampleID_submission.x, .keep_all = TRUE) %>%
    group_by(Other_sampleID.x) %>%
    mutate(Replicate = row_number()) %>%
    ungroup() %>%
    transmute(
      `*sample_name`        = SampleID_submission.x,
      sample_title          = paste0(LK500_ID, " ", Tissue, " ", Treatment, " replicate ", Replicate),
      bioproject_accession  = NA,
      `*organism`           = SpeciesID,
      isolate               = NA,
      cultivar              = Other_lineID,
      ecotype               = NA,
      age                   = Age_plants_in_days,
      dev_stage             = Plant_structure_development_stage,
      `*collection_date`    = format(as.Date(as.character(Date_plant_collection), "%Y%m%d"), "%Y-%m-%d"),
      `*geo_loc_name`       = "Netherlands",
      `*tissue`             = Tissue,
      biomaterial_provider  = NA,
      cell_line             = NA,
      cell_type             = NA,
      collected_by          = NA,
      culture_collection    = NA,
      disease               = NA,
      disease_stage         = NA,
      genotype              = CGN_ID,
      growth_protocol       = NA,
      height_or_length      = NA,
      isolation_source      = NA,
      lat_lon               = NA,
      phenotype             = NA,
      population            = NA,
      sample_type           = NA,
      sex                   = NA,
      specimen_voucher      = NA,
      temp                  = NA,
      treatment             = Treatment,
      description           = NA,
      # ── extra columns ──────────────────────────────
      Replicate             = Replicate,
      plant_structure       = Plant_anatomy
    )
}

# Apply per experiment
biosample_results <- list()
for (exp_name in names(csv_list)) {
  
  element <- csv_list[[exp_name]]
  
  if (!is.data.frame(element)) {
    cat("Skipping", exp_name, "— not a data frame (class:", class(element), ")\n")
    next
  }
  
  biosample_results[[exp_name]] <- build_biosample_df(element)
  cat(exp_name, ":", nrow(biosample_results[[exp_name]]), "samples\n")
}

# Save per experiment into SRA BioSample template
for (exp_name in names(biosample_results)) {
  
  wb_biosample <- loadWorkbook(sra_template)
  sheet_name   <- sheets(wb_biosample)[1]
  
  df <- biosample_results[[exp_name]]
  
  # ── 1. Write the standard BioSample block (columns 1–32, no header) ──────
  standard_cols <- df[, 1:32]
  
  writeData(wb_biosample,
            sheet    = sheet_name,
            x        = standard_cols,
            startRow = 14,
            startCol = 1,
            colNames = FALSE)
  
  # ── 2. Write extra columns starting right after the standard block ────────
  extra_cols     <- df[, c("Replicate", "plant_structure")]
  extra_start_col <- ncol(standard_cols) + 1   # column 33
  
  # Write headers for the extra columns (once, in the row just above data)
  writeData(wb_biosample,
            sheet    = sheet_name,
            x        = extra_cols,
            startRow = 13,             # header row just above your data rows
            startCol = extra_start_col,
            colNames = TRUE)           # TRUE so column names are written as header
  
  saveWorkbook(wb_biosample,
               file      = paste0(out_dir, exp_name, "_BioSample_attributes.xlsx"),
               overwrite = TRUE)
  
  cat("Saved:", paste0(exp_name, "_BioSample_attributes.xlsx"),
      "—", nrow(df), "samples\n")
}

# Save per experiment as TSV for SRA upload
for (exp_name in names(biosample_results)) {
  
  df_tsv <- biosample_results[[exp_name]]
  colnames(df_tsv) <- str_remove(colnames(df_tsv), "^\\*")  # strip leading *
  
  write_tsv(df_tsv,
            file = paste0(out_dir, exp_name, "_BioSample_attributes.tsv"),
            na = "")
  
  cat("Saved:", paste0(exp_name, "_BioSample_attributes.tsv"), "\n")
}
2. Wron