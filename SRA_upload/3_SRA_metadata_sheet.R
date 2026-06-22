# ============================================================
# SRA Submission Prep Script — batch version
# ============================================================
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
  
  # -- Load & filter I1/I2 index reads 
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
    file_path   = meta_filtered$file_path
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
    select(file_path, Other_sampleID.x) %>%
    distinct()
  
  sra_df %>%
    left_join(other_id_lookup, by = c("file_path1" = "file_path")) %>%
    transmute(
      sample_name        = sample_name,
      library_ID         = library_ID,
      title              = paste0("RNA-seq", Other_sampleID.x),
      library_strategy   = "ssRNA-seq",
      library_source     = "TRANSCRIPTOMIC",
      library_selection  = "PolyA",
      library_layout     = "paired",
      platform           = "ILLUMINA",
      instrument_model   = "NextSeq 2000",
      design_description = "NA",
      filetype           = "fastq",
      filename           = filename1,
      filename2          = filename2,
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
            x        = sra_results[[exp_name]],   # index into list with [[exp_name]]
            startRow = 3,
            startCol = 1,
            colNames = FALSE)
  
  saveWorkbook(wb_sra,
               file      = paste0(out_dir, exp_name, "_SRA_metadata.xlsx"),
               overwrite = TRUE)
  
  cat("Saved:", paste0(exp_name, "_SRA_metadata.xlsx"), "\n")
}




# -- 3.5 Save into SRA template -----------------------------
wb_sra <- loadWorkbook(sra_template)
sheet_name <- sheets(wb_sra)[2]  # check with sheets(wb_sra) if unsure
writeData(wb_sra,
          sheet    = sheet_name,
          x        = sra_results,
          startRow = 3,           
          startCol = 1,
          colNames = FALSE)
saveWorkbook(wb_sra,
             file      = paste0(out_dir, exp_name, "_SRA_metadata.xlsx"),
             overwrite = TRUE)



############################
############################

pair_reads <- function(df, library_id_suffix = "") {
  
  # Return empty df if input is empty (e.g. no additional-sequencing files)
  if (nrow(df) == 0) return(data.frame())
  
  sra <- data.frame(
    sample_name        = df$SampleID_submission.x,
    library_ID         = paste0(str_remove(df$name_no_ext, "_(R1|R2).*$"), library_id_suffix),
    title              = str_remove(df$name_no_ext, "_(R1|R2).*$"),
    library_strategy   = "ssRNA-seq",
    library_source     = "TRANSCRIPTOMIC",
    library_selection  = "PolyA",
    library_layout     = "paired",
    platform           = "ILLUMINA",
    instrument_model   = "NextSeq 2000",       # adjust if needed
    design_description = "NA",                 # adjust if needed
    filetype           = "fastq",
    filename           = df$full_name,
    assembly           = NA,
    fasta_file         = NA
  )
  
  r1 <- sra %>%
    filter(str_detect(filename, "_R1_")) %>%
    mutate(pair_key = str_remove(filename, "_R1_.*$"))
  
  r2 <- sra %>%
    filter(str_detect(filename, "_R2_")) %>%
    select(filename) %>%
    rename(filename2 = filename) %>%
    mutate(pair_key = str_remove(filename2, "_R2_.*$"))
  
  r1 %>%
    left_join(r2, by = "pair_key", relationship = "one-to-one") %>%
    select(-pair_key) %>%
    mutate(filename3 = NA, filename4 = NA) %>%
    select(sample_name, library_ID, title, library_strategy, library_source,
           library_selection, library_layout, platform, instrument_model,
           design_description, filetype, filename, filename2, filename3,
           filename4, assembly, fasta_file)
}

# ---- 3. BATCH LOOP ------------------------------------------
csv_files <- list.files(in_dir, pattern = "\\.csv$", full.names = FALSE)

for (csv_file in csv_files) {
  
  exp_name <- str_remove(csv_file, "\\.csv$")  # e.g. "ExpMA002"
  cat("Processing:", exp_name, "\n")
  
  # -- 3.1 Load & filter I1/I2 index reads --------------------
  meta <- read_csv(paste0(in_dir, csv_file), show_col_types = FALSE)
  
  meta_filtered <- meta %>%
    filter(!str_detect(basename(name_no_ext), "_(I1|I2)_"))
  
  # -- 3.2 Split original and additional-sequencing runs ------
  meta_original   <- meta_filtered %>% filter(!str_detect(file_path, "additional-sequencing_"))
  meta_additional <- meta_filtered %>% filter( str_detect(file_path, "additional-sequencing_"))
  
  cat("  Original rows:", nrow(meta_original),
      "| Additional rows:", nrow(meta_additional), "\n")
  
  # -- 3.3 Pair R1/R2 and bind; additional rows get _add-seq suffix
  paired_original   <- pair_reads(meta_original,   library_id_suffix = "")
  paired_additional <- pair_reads(meta_additional, library_id_suffix = "_add-seq")
  
  cat("  Original pairs:", nrow(paired_original),
      "| Additional pairs:", nrow(paired_additional), "\n")
  
  sra_df_v2 <- bind_rows(paired_original, paired_additional) %>%
    arrange(sample_name)
  
  cat("  Total paired samples (incl. add-seq):", nrow(sra_df_v2), "\n")
  
  # -- 3.4 Build file path data frame -------------------------
  df_path <- data.frame(
    sample_name = meta_filtered$SampleID_submission.x,
    library_ID  = meta_filtered$name_no_ext,
    full_name   = meta_filtered$full_name,
    file_path   = meta_filtered$file_path
  )
  
