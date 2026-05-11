# LettuceKnow Data Inventory & Organisation

The LettuceKnow consortium data are stored in the Yoda file management system. Yoda is based on iRODS, and interaction with its backend is possible via the iCommands suite.

Basic explanations of iRODS, relevant iCommands, and the setup of a virtual machine (VM) to directly interact with Yoda are provided in the following documents, which are maintained in a separate GitHub repository:

1. [Setting up VM](https://github.com/melanorian/bio_methods/blob/main/VM_set-up_Linux_VirtualBox.md)

2. [iRODS & iCommands](https://github.com/melanorian/bio_methods/blob/main/iCommands-for-YODA_iRODS.md)

## Index

[Workstream A: Inventory of Data on YODA](#workstream-a-inventory-of-data-on-yoda)

[Step 1: Generate Full YODA Collection Inventory](#step-1-generate-full-yoda-collection-inventory)

[Step 2: Processing Inventory CSVs & Generating Subcollection Summaries](#step-2-processing-inventory-csvs-generating-subcollection-summaries)

[Step 3: Processing Inventory CSVs & Generating File Type Summaries](#step-3-processing-inventory-csvs-generating-file-type-summaries)

[Step 4: Generate CSV file with Inventory Size and File Types](#step-4-generate-csv-file-with-inventory-size-and-file-types)

[Step 5: Enrich Inventory with Documentation & Informative Files](#step-5-enrich-inventory-with-documentation-and-informative-files)

[Step 5a: Optional – Extract File-Level Inventory for a Specific Collection](#step-5a-optional-extract-file-level-inventory-for-a-specific-collection)

[Step 6: Summarize Inventory to Nearest Sub-Collection Level](#step-6-summarize-inventory-to-nearest-sub-collection-level)

[Step 7: Duplicate File Detection](#step-7-duplicate-file-detection)

[Step 7b: Prioritize Duplicate Files for Potential Deletion](#step-7b-prioritize-duplicate-files-for-potential-deletion)

[Step 7c: Visualize Duplicate Storage and Potential Deletion Candidates](#step-7c-visualize-duplicate-storage-and-potential-deletion-candidates)

[Step 8: Integrate Duplicate Statistics into Collection-Level Inventory](#step-8-integrate-duplicate-statistics-into-collection-level-inventory)

[Step 9: Classify Collections by Processing Level Domain and Release Status](#step-9-classify-collections-by-processing-level-domain-and-release-status)

[Step 10: Visualize Storage Distribution Across Releases Domains and Processing Levels](#step-10-visualize-storage-distribution-across-releases-domains-and-processing-levels)

## Workstream A: Inventory of Data on YODA 

### Step 1: [Generatefull YODA Collection Inventory](https://github.com/melanorian/LK_data-work/blob/main/inventory_yoda.sh)

This script creates a **CSV inventory** of files in a Yoda/iRODS collection using `iquest`. It queries the iCAT catalog directly, making it efficient for large datasets.

**Input**

- `base_collection` - path to the iRODS collection you want to inventory
- Header, format, and query lines - Default with creation time (comment to deactivate with "#"), alternative: without creation time (uncomment to activate removing "#")
- Active iRODS session (`iinit`)  
- Optional: uncomment alternate query to include `DATA_CREATE_TIME`

**Output**

- CSV file: `./inventory_<basename of collection>/inventory.csv`  
- Log file: `./inventory_<basename of collection>/inventory.log`

**What it does:**

- Extracts file metadata:
  - Collection path (`COLL_NAME`)
  - File name (`DATA_NAME`)
  - File size in bytes (`DATA_SIZE`)
  - Replica number (`DATA_REPL_NUM`)
  - Checksum (`DATA_CHECKSUM`)
  - Creation time (`DATA_CREATE_TIME`) – optional  (change in script)
- Saves results to a CSV file
- Writes a log file with execution details

**Notes**

- iRODS DATA_CREATE_TIME is returned as a Unix timestamp-like integer - requires downstream conversion. E.g. 01727370936 == Thu Sep 26 2024 19:15:36 GMT+0200 (Central European Summer Time)
- File sizes are reported in **bytes**  
- Only accessible files can be included

### Step 2: [Processing Inventory CSVs & Generating Subcollection Summaries](https://github.com/melanorian/LK_data-work/blob/main/2_process_inventory_csv.py)

This Python script summarizes LettuceKnow inventory CSVs into subcollection table with aggregated file sizes up to a manually defined maximum depth of sub-collections. 

**Input Variables**

- `BASE_DIR` – directory containing inventory CSVs (`inventory_<collection>/inventory.csv`)  
- `OUT_DIR` – output directory for subcollection summary CSV  
- `IGNORE_PRE` – path prefix to remove from file paths (optional)  
- `MAX_LEVEL` – depth of subcollection aggregation  

**Output**

- Combined inventory table (`full_df` internally)  
- Subcollection summary CSV: `subcollection_summary_L<MAX_LEVEL>.csv` containing:  
  - `collection` – subcollection path  
  - `collection_size_bytes` – cumulative size including nested files  
  - `num_files` – total number of files  
  - `collection_size_GB` / `collection_size_TB` – size in convenient units  

**What it does**

1. Read CSVs & fix headers
   - Automatically merge `COLL_NAME` + `DATA_NAME` into `COLL_NAME`.

2. Validate column consistency
   - Ensure all CSVs have the same structure before combining.

3. Combine CSVs
   - Merge into a single DataFrame and convert `DATA_SIZE` to numeric.

4. Normalize paths
   - Strip `IGNORE_PRE` prefix and split paths into components.

5. Define subcollection keys
   - Identify subcollections at the specified `MAX_LEVEL`.

6. Aggregate & summarize data
   - Compute total size and file count per subcollection, including cumulative sizes for parent directories.  
   - Save the resulting summary CSV to `OUT_DIR` with filename `subcollection_summary_L<MAX_LEVEL>.csv`.

### Step 3: [Processing Inventory CSVs & Generating File Type Summaries](https://github.com/melanorian/LK_data-work/blob/main/3_inventory_data-type.py)

This Python script analyzes LettuceKnow inventory CSVs to summarize **file type distributions** across subcollections and globally. It provides insight into the composition of data (e.g. sequencing files, reports, archives) within the Yoda environment.

**Input Variables**

- `BASE_DIR` – directory containing inventory CSVs (`inventory_<collection>/inventory.csv`)  
- `OUT_DIR` – output directory for file type summaries  
- `IGNORE_PRE` – path prefix to remove from file paths (optional)  
- `MAX_LEVEL` – depth of directory structure used to define aggregation branches  

**Output**

- Branch-level file type summary:  
  - `file-type_inventory_L<MAX_LEVEL>.csv` containing:  
    - `BRANCH` – subcollection path up to `MAX_LEVEL`  
    - `num_files` – total number of files in the branch  
    - `file_types` – JSON dictionary of file extensions and their respective counts  

- Global file type summary:  
  - `file-type_summary_L<MAX_LEVEL>.csv` containing:  
    - `file_type` – detected file extension  
    - `total_count` – total occurrences across all files  
    - `num_branches` – number of branches in which the file type appears  

**What it does**

1. Locate and read inventory CSVs  
   - Recursively searches `BASE_DIR` for `inventory.csv` files.  
   - Merges all valid CSVs into a single DataFrame for analysis.

2. Extract file types  
   - Derives file extensions from file names.  
   - Handling of multi-part extensions (e.g. `.fastq.gz`, `.tsv.gz`).  
   - Assigns `"no_ext"` where no extension is present, e.g for (sub-)collections

3. Define aggregation branches  
   - Groups files by directory structure up to `MAX_LEVEL`.

4. Aggregate branch-level summaries  
   - Counts total files per branch.  
   - Computes count of file types within each branch.

5. Generate global file type statistics  
   - Aggregates counts of each file type across all branches.  

6. Save outputs  
   - Writes both branch-level and global summaries to `OUT_DIR`.

**Notes**

- File types are inferred from filenames and may include artifacts due to naming inconsistencies.  
- Multi-part extensions are partially normalized but not fully standardized (e.g. `.vcf.gz` vs `.gz`).  
- The branch-level JSON structure enables flexible downstream parsing and categorization.  
- The global summary is useful for identifying dominant file types for further data classification.

### Step 4: [Generate CSV file with Inventory Size and File Types](https://github.com/melanorian/LK_data-work/blob/main/4_merge_inventory_outputs.py)

Branch-level file type summaries and subcollection summaries Steps 2 & 3, are merged to provide a combined view of size and file type composition per branch.


**Input Variables**

- `BASE_DIR` – directory containing:
  - `subcollection_summary_L<MAX_LEVEL>.csv`
  - `file-type_inventory_L<MAX_LEVEL>.csv`
  - Optional: `file-type_summary_L4.csv` (file type descriptions annotated by pasting into chatGPT)
- `MAX_LEVEL` – depth of branch aggregation used in previous scripts  
- `OUT_FILE` – path to save merged inventory CSV  

**What it does**

1. Loads branch-level file type data and subcollection size data.  
2. Validates uniqueness of branch keys (`collection`) in both tables.  
3. Loads optional file type description table to provide human-readable descriptions, this file was annotated manually by copy-paste into chatGPT.  
4. Merges the two datasets on `collection`, keeping all rows and reporting any mismatches.  
5. Sorts the merged table by `collection` for readability.  
6. Adds a column `file_type_description`:
   - Converts JSON dictionary of file types per branch into an array of **unique descriptions**
   - Maintains order and removes duplicates
   - Unknown file types are labeled `"NA"`  
7. Saves the final merged table to CSV.

**Output**

- `merged_inventory_L<MAX_LEVEL>.csv` containing:
  - `collection` – branch/subcollection path  
  - `collection_size_bytes` – cumulative size of files in the branch  
  - `collection_size_GB` / `collection_size_TB` – convenient units  
  - `num_files` – total number of files in the branch  
  - `file_types` – JSON dictionary of file extensions and counts  
  - `file_type_description` – JSON array of unique descriptions  

**Notes**

- The merge allows quick inspection of both storage footprint and data composition per branch.  
- If descriptions for some file types are missing, `"NA"` will be shown.

### Step 5: [Enrich Inventory with Documentation & Informative Files](https://github.com/melanorian/LK_data-work/blob/main/5_documentation_quality.py) 

This Python script annotates the merged LettuceKnow inventory with the presence of **informative files** such as README, log, configuration, and metadata files at the collection level. It combines collection-level summaries with file-level classifications to provide insight into available documentation and supporting files.

**Input Variables**

- `BASE_DIR` – directory containing file-level inventory CSVs (`inventory_<collection>/inventory.csv`)  
- `REPORT_DIR` – directory containing merged collection-level inventory CSV (`merged_inventory_L<MAX_LEVEL>.csv`)  
- `MAX_LEVEL` – depth used to define collections consistently with previous steps  
- `MERGED_FILE` – merged inventory CSV from Step 4  
- `OUT_FILE` – path to save the enriched collection-level inventory  

**Output**

- CSV file: `merged_inventory_with_docs_L<MAX_LEVEL>.csv` containing:
  - Original collection-level information (from merged inventory)
  - Aggregated counts per collection of:
    - `README` – number of README files present
    - `log` – number of log files (e.g., `.log`, `.out`, `.err`)
    - `config` – number of configuration files (e.g., `.cfg`, `.ini`, `.yaml`, `.yml`)
    - `metadata` – number of metadata files (e.g., `.json`, `.xml`, `.tsv`, `.csv`)  

**What it does**

1. **Load merged collection inventory**
   - Reads the merged collection-level CSV produced in Step 4.
2. **Load file-level inventories**
   - Reads all inventory CSVs from the base directory and concatenates them.
   - Standardizes column naming to match previous steps.
3. **Define collection keys**
   - Generates consistent collection paths up to `MAX_LEVEL` to match Step 4 aggregation.
4. **Classify informative files**
   - Examines file names and extensions to detect README, log, config, and metadata files.
5. **Aggregate per collection**
   - Sums the classified informative files for each collection.
6. **Merge with existing collection data**
   - Combines aggregated counts with the merged collection-level inventory.
   - Fills missing values with 0 for collections without any informative files.
7. **Save enriched inventory**
   - Writes the output CSV to `OUT_FILE` in `REPORT_DIR`.

**Notes**
- Only informative files with recognized patterns/extensions are counted.

### Step 5a: [Optional – Extract File-Level Inventory for a Specific Collection](https://github.com/melanorian/LK_data-work/blob/main/YODA_Inventory/5a_optional_files_in_target_collection.py)

This Python script generates a **file-level inventory CSV** for a specific subcollection of interest within the LettuceKnow data, e.g., RNA-seq data.

**Input Variables**

- `BASE_DIR` – directory containing all inventory CSVs (`inventory_<collection>/inventory.csv`)
- `TARGET_COLLECTION` – relative path of the subcollection to filter (e.g., `research-lettuceknow/processed_data/rnaseq`)
- `OUT_DIR` – output directory for the resulting CSV  

**Output**

- `optional1_rnaseq_file_level_inventory.csv` – contains all files from the target collection, including:
  - `COLL_NAME` – full iRODS collection path
  - `DATA_NAME` – file name
  - `DATA_SIZE` – size in bytes
  - `DATA_CHECKSUM` – file checksum
  - Any other metadata available in the original CSVs

**What it does**

1. Locates all inventory CSV files in `BASE_DIR`.
2. Reads each CSV and fixes the combined `COLL_NAME/DATA_NAME` header.
3. Combines all CSVs into a single DataFrame.
4. Normalizes paths by removing the prefix `/nluu6p/home/`.
5. Filters rows to keep only files within the `TARGET_COLLECTION`.
6. Saves the filtered DataFrame to `OUT_DIR` as a CSV for downstream analysis.

**Notes**

- Useful for focusing on a single experiment or data type without processing the entire dataset.
- Works at **file-level granularity**, not aggregated collections.
- Optional: can be run multiple times for different target collections.

### Step 6: [Summarize Inventory to nearest sub-collection level](https://github.com/melanorian/LK_data-work/blob/main/6_summarise_to_subcollection.py)

This Python script takes the enriched merged inventory from Step 5 and **aggregates file-level to collection-level information** to produce a summarized view of the data. This is neccesary because the depth of sub-collections is very uneven and some sub-collections list all the files. Here, we computes cumulative sizes, file counts, documentation indicators, and file type distributions to the defined collection levels.
 
**Input Variables**

- `BASE_DIR` – directory containing enriched inventory CSV (`merged_inventory_with_docs_L<MAX_LEVEL>.csv`)  
- `MAX_LEVEL` – depth used in collection aggregation  
- `INPUT_FILE` – merged inventory with documentation indicators from Step 5  
- `OUT_FILE` – path to save the summarized collection-level inventory  

**Output**

- CSV file: `summarized_inventory_L<MAX_LEVEL>.csv` containing:
  - `collection` – deepest collection path
  - `num_files` – total number of files in the collection (aggregated from file-level inventories)
  - `collection_size_bytes` – cumulative size in bytes
  - `collection_size_GB` / `collection_size_TB` – sizes converted to convenient units
  - `README`, `log`, `config`, `metadata` – counts of informative files per collection
  - `file_types` – JSON dictionary summarizing file types and counts  

**What it does**

1. **Load enriched inventory**
   - Reads the CSV produced in Step 5.
   - Ensures that documentation columns (`README`, `log`, `config`, `metadata`) exist.
2. **Identify file-level rows**
   - Determines which rows correspond to files vs collections using path suffixes.
   - Preserves original parent collection size info and counts of child files.
3. **Filter pre-aggregated collection rows**
   - Removes non-file rows that are already represented in file-level aggregation to avoid double-counting.
4. **Define summarized collection paths**
   - Sets a consistent collection key for aggregation, corresponding to parent directories for file rows.
5. **Prepare file type dictionaries**
   - Safely loads JSON dictionaries of file types from the inventory.
   - Ensures numeric columns are correctly typed for aggregation.
6. **Aggregate file-level and collection-level data**
   - Uses `groupby` and custom aggregation functions (`sum` for numeric columns, `Counter` merge for file types).
   - Applies fixes for special cases (e.g., collections with zero size but known parent size).
7. **Compute additional metrics**
   - Converts collection sizes into GB and TB.
   - Converts aggregated file type dictionaries back to JSON strings.
8. **Filter to deepest collections**
   - Keeps only the most granular collection paths to avoid redundancy.
   - Removes trivial system files like `.DS_Store`, `Thumbs.db`, and `Desktop.ini`.
9. **Save summarized dataset**
   - Writes the final summarized inventory CSV to `OUT_FILE`.

**Notes**
- JSON-formatted `file_types` allow flexible parsing and querying of file compositions per collection.

### Step 7: [Duplicate File Detection](https://github.com/melanorian/LK_data-work/blob/main/7_duplicat_detection.py)

This Python script analyzes all LettuceKnow inventory CSVs to **detect duplicate files** based on file names and checksums. It assigns consistent group IDs to files that are identical or share the same name, enabling downstream auditing and quality control.

**Input Variables**

- `BASE_DIR` – directory containing inventory CSVs (`inventory_<collection>/inventory.csv`)  
- `OUT_DIR` – directory to save the duplicate detection report  
- `IGNORE_PRE` – optional path prefix to remove from file paths  

**Output**

- CSV file: `duplicate_detection.csv` containing:
  - `file_name` – full relative path of the file
  - `DATA_SIZE` – size in bytes
  - `checksum` – file checksum (if available)
  - `dup_checksum` – `True` if the checksum is duplicated across files
  - `dup_name` – `True` if the file name (including extension) is duplicated
  - `dup_both` – `True` if both checksum and name are duplicated
  - `dup_group_id` – numeric ID assigned to each duplicate group (same for files with same name or checksum)  

**What it does**

1. **Locate and read inventory CSVs**
   - Recursively searches `BASE_DIR` for `inventory.csv` files.
   - Fixes header inconsistencies (`COLL_NAME,DATA_NAME` → `COLL_NAME/DATA_NAME`) and reads all CSVs into a unified DataFrame.
2. **Normalize file paths**
   - Strips optional `IGNORE_PRE` prefix for consistent relative paths.
3. **Filter file-level rows**
   - Keeps only actual files, excluding trivial system files like `.DS_Store`, `Thumbs.db`, and `Desktop.ini`.
4. **Extract file names**
   - Derives `file_name_only` from the full path for duplicate detection by name.
5. **Handle checksums**
   - Fills missing checksums with empty strings.
   - Detects duplicates by checksum, by file name, and by both.
6. **Assign duplicate group IDs**
   - Files with the same checksum get the same group ID.
   - Files with the same name (if not already grouped by checksum) also get the same group ID.
   - Ensures each group has a unique numeric ID for easy reference.
7. **Prepare final output**
   - Includes relevant duplicate flags, group IDs, file sizes, and checksums.
   - Sorts the CSV first by duplicate flags and group IDs to simplify inspection.
8. **Save output**
   - Writes a structured CSV to `OUT_DIR/duplicate_detection.csv` for auditing and further analysis.

**Notes**
- Group IDs are **consistent across all files sharing the same name or checksum**, allowing easy identification of duplicates.
- Sorting by `dup_both`, `dup_checksum`, `dup_name`, and `dup_group_id` ensures that related duplicates appear together in the CSV for rapid manual inspection.

### Step 7: [Duplicate File Detection](https://github.com/melanorian/LK_data-work/blob/main/YODA_Inventory/7_duplicat_detection.py)

This Python script analyzes all LettuceKnow inventory CSVs to detect potentially duplicate files using both file names and checksums. The goal is not only strict checksum duplication detection, but also identification of files with identical basenames occurring across different storage locations and releases.

Unlike earlier implementations, filename-based and checksum-based duplicate detection are intentionally combined into a shared duplicate grouping system to support large-scale inventory cleanup and release comparison.

**Input Variables**

- `BASE_DIR` – directory containing inventory CSVs (`inventory_<collection>/inventory.csv`)
- `OUT_DIR` – directory to save the duplicate detection report
- `IGNORE_PRE` – optional path prefix to remove from file paths

**Output**

- CSV file: `7_duplicate_detection.csv` containing:
  - `file_path` – full iRODS file path
  - `basename` – filename only
  - `DATA_SIZE` – file size in bytes
  - `DATA_CHECKSUM` – checksum if available
  - `storage_location` – top-level storage category
  - `dup_name` – `True` if basename occurs multiple times
  - `dup_checksum` – `True` if checksum occurs multiple times
  - `dup_any` – `True` if duplicate by either checksum or basename
  - `dup_group_id` – shared duplicate group identifier
  - `duplicate_group_size` – number of rows in the duplicate group

**What it does**

1. **Locate and read inventory CSVs**

2. **Identify file-level rows**
   - Keeps only rows representing files.
   - Excludes collection-only entries.

3. **Extract duplicate-relevant metadata**
   - Creates:
     - `file_path`
     - `basename`
     - normalized checksum field

4. **Duplicate identity and categories**
   - Uses checksum as primary identity when available.
   - Falls back to basename when checksum is missing.

5. **Assign duplicate groups**
   - Files sharing the same checksum or basename receive the same `dup_group_id`.
   - Group sizes are computed across the full dataset.

6. **Annotate storage location**
   - Labels rows as:
     - `research-lettuceknow`
     - `research-lettuceknow-releases`

**Notes**

- Files without checksums are still grouped by basename.
- Large duplicate groups may occur for common technical output files generated repeatedly across sequencing runs or QC workflows!

### Step 7b: [Prioritize Duplicate Files for Potential Deletion](https://github.com/melanorian/LK_data-work/blob/main/YODA_Inventory/7b_duplicats_in_release-and-dump.py)

This Python script extends the duplicate detection results from Step 7 by assigning a **storage tier priority** to duplicate groups and marking lower-priority copies as potential deletion candidates.

The script does **not delete any files**.  It only annotates duplicate records with a boolean column indicating whether a file is considered redundant according to release hierarchy rules.

**Priority hierarchy**

Highest-quality / newest copies are preferred:

1. `data-release_V2`
2. `data-release_V1`
3. `research-lettuceknow`

Files in lower-priority locations are marked as potential deletion candidates if a higher-priority copy exists within the same duplicate group.

**Input Variables**

- `BASE_DIR` – directory containing duplicate detection output from Step 7  
- `INPUT_FILE` – `7_duplicate_detection.csv`
- `OUT_FILE` – annotated duplicate table with deletion recommendations

**Output**

- CSV file: `7b_delete_duplicates.csv` containing:
  - Original duplicate detection columns from Step 7
  - `priority` – numeric storage priority:
    - `3` = DR2
    - `2` = DR1
    - `1` = research storage
  - `max_priority_in_group` – highest priority observed within the duplicate group
  - `delete_duplicate` – `True` if a higher-priority copy exists elsewhere in the group

**What it does**

1. Loads duplicate detection output from Step 7.
2. Assigns storage priority levels based on file path patterns.
3. Computes the highest priority present in each duplicate group.
4. Marks files as potential deletion candidates if: their priority is lower than the maximum priority within the group.

**Example**

If the same file exists in:

- `research-lettuceknow`
- `data-release_V1`
- `data-release_V2`

then:

- DR2 copy → retained (`delete_duplicate = False`)
- DR1 copy → candidate for deletion (`True`)
- research copy → candidate for deletion (`True`)

If the file exists only in:

- `research-lettuceknow`
- `data-release_V1`

then:

- DR1 copy → retained
- research copy → candidate for deletion

**Notes**

- Duplicate grouping logic from Step 7 is preserved = the same problem applies: large duplicate groups may occur for common technical output files generated repeatedly across sequencing runs or QC workflows!
- Duplicate groups may still contain biologically distinct files with identical names when checksums are unavailable.
- Manual validation before any deletion!

### Step 7c: [Visualize Duplicate Storage and Potential Deletion Candidates](https://github.com/melanorian/LK_data-work/blob/main/YODA_Inventory/7c_visualise_duplicates.py)

This Python script visualizes the duplicate analysis results from Step 7b using pie charts. It summarizes the amount of storage occupied by duplicate files and highlights which portions are considered potential deletion candidates.

**Input Variables**

- `BASE_DIR` – directory containing duplicate analysis outputs
- `INPUT_FILE` – `7b_delete_duplicates.csv`
- `OUT_DIR` – directory where SVG visualizations are saved

**Output**

SVG figures stored in:

`<BASE_DIR>/visualisation/`

Generated files:

1. `7c_pie_delete_duplicates.svg`
   - Pie chart showing:
     - storage potentially deletable
     - storage retained

2. `7c_pie_delete_duplicates_by_tier.svg`
   - Pie chart showing deletable duplicate storage split by storage tier:
     - `research-lettuceknow`
     - `research-lettuceknow-release_V1`
     - `research-lettuceknow-release_V2`

**What it does**

1. Loads duplicate annotation output from Step 7b.
2. Creates a global duplicate-storage summary:
   - total deletable storage
   - total retained storage
3. Generates a pie chart visualizing:
   - percentage of deletable duplicate storage
   - percentage of retained storage
4. Generates a second pie chart showing the distribution of deletable storage across:
   - DR2
   - DR1
   - research storage

### Step 8: [Integrate Duplicate Statistics into Collection-Level Inventory](https://github.com/melanorian/LK_data-work/blob/main/8_summarized_inventory_with_duplicates.py](https://github.com/melanorian/LK_data-work/blob/main/YODA_Inventory/8_merge_duplicates_add_costs.py)

This Python script integrates duplicate-file statistics from Step 7 into the summarized collection-level inventory produced in Step 6. The resulting table allows duplicate burden to be analyzed at collection level.


**Input Variables**

- `BASE_DIR` – directory containing summarized inventory and duplicate detection outputs
- `MAX_LEVEL` – collection aggregation depth used in previous steps
- `SUMMARY_FILE` – `summarized_inventory_L<MAX_LEVEL>.csv`
- `DUP_FILE` – duplicate detection output from Step 7
- `OUT_FILE` – merged collection-level inventory with duplicate statistics

---

**Output**

- CSV file:
  `8_summarized_inventory_with_duplicates_L<MAX_LEVEL>.csv`

Additional duplicate-related columns include:

- `num_dup_checksum`
- `num_dup_name`
- `num_dup_any`
- `num_files_in_dup_check`
- `collection_dup_size_bytes_checksum`
- `collection_dup_size_bytes_name`
- `collection_dup_size_bytes_any`
- Corresponding GB and TB columns

**What it does**

1. Loads:
   - summarized collection inventory from Step 6
   - duplicate detection output from Step 7
2. Maps each file to its deepest matching summarized collection.
3. Removes files that cannot be mapped to a summarized collection.
4. Ensures file sizes are numeric.
5. Aggregates duplicate statistics per collection:
   - duplicate counts by checksum
   - duplicate counts by basename
   - duplicate counts by combined duplicate identity
   - cumulative duplicate storage sizes
6. Converts duplicate storage sizes to:
   - GB
   - TB
7. Merges duplicate summaries into the collection-level inventory.
8. Fills missing duplicate statistics with zero.
9. Saves the merged collection inventory.

**Notes**

- Duplicate statistics reflect file-level duplicate detection from Step 7.
- Collection sizes themselves are not modified.

### Step 9: [Classify Collections by Processing Level, Domain, and Release Status](https://github.com/melanorian/LK_data-work/blob/main/YODA_Inventory/9_classify_files.py)

This Python script classifies summarized LettuceKnow collections into broad biological and processing-related categories. The classification provides higher-level semantic annotation for downstream reporting and visualization.

**Input Variables**

- `BASE_DIR` – directory containing summarized inventory with duplicate information
- `MAX_LEVEL` – collection aggregation depth
- `SUMMARY_FILE` – `8_summarized_inventory_with_duplicates_L<MAX_LEVEL>.csv`
- `OUT_FILE` – classified inventory output

**Output**

- CSV file:
  `9_summarized_inventory_classified_L<MAX_LEVEL>.csv`

Additional annotation columns include:

- `processing_level`
- `data_domain`
- `special_category`
- `released`
- `release_version`

**What it does**

1. Loads summarized inventory with duplicate annotations from Step 8.
2. Parses JSON-formatted file type summaries.
3. Classifies collections into processing levels:
   - `raw_data`
   - `processed_data`
   - `results_data`
   - `release_data`
   - `mixed_or_unknown`
4. Classifies collections into scientific domains:
   - `RNA`
   - `DNA`
   - `phenotyping`
   - `unknown`
5. Detects special categories such as:
   - transfer tests
   - third-party data
   - manually marked deletion folders
6. Determines release status:
   - non-release
   - DR1
   - DR2
7. Prints overview statistics for quick inspection.
8. Saves the classified inventory table.

**Notes**

- Classification is rule-based and path-driven.
- File-type information is used as supplementary evidence.
- Categories are intentionally broad to support high-level reporting.
- Collections may still contain heterogeneous data types despite classification.

### Step 10: [Visualize Storage Distribution Across Releases, Domains, and Processing Levels](https://github.com/melanorian/LK_data-work/blob/main/YODA_Inventory/10_overview_visualisation_inventory.py)

This Python script generates summary visualizations for the classified LettuceKnow inventory produced in Step 9. The figures provide an overview of storage distribution across release status, scientific domains, and processing stages.

**Input Variables**

- `base_dir` – directory containing classified inventory outputs
- `input_file` – `9_summarized_inventory_classified_L5.csv`
- `out_dir` – directory where SVG figures are saved

**Output**

SVG figures saved to:

`<base_dir>/visualisation/`

Generated figures:

1. `pie_release_status.svg`
   - Storage distribution by:
     - non-release
     - DR1
     - DR2

2. `pie_domain_all.svg`
   - Storage distribution across scientific domains

3. `pie_processing_level.svg`
   - Storage distribution across processing stages

4. `stacked_processing_by_domain.svg`
   - Stacked bar chart showing processing level per scientific domain

**What it does**

1. Loads classified inventory from Step 9.
2. Normalizes missing values in:
   - release annotations
   - domain annotations
   - processing-level annotations
3. Generates helper labels containing:
   - approximate TB values
   - percentages
4. Creates a pie chart summarizing release storage distribution.
5. Creates a pie chart summarizing scientific domains.
6. Creates a pie chart summarizing processing levels.
7. Creates a stacked bar chart comparing:
   - processing level
   - scientific domain
8. Saves all visualizations as SVG files.

**Notes**

- Storage sizes are based on cumulative collection sizes.
- Percentages are calculated from total summarized storage.
- Visualizations are intended for high-level reporting and exploratory analysis.
