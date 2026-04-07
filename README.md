A# LettuceKnow Data Inventory & Organisation

The LettuceKnow consortium data are stored in the Yoda file management system. Yoda is based on iRODS, and interaction with its backend is possible via the iCommands suite.

Basic explanations of iRODS, relevant iCommands, and the setup of a virtual machine (VM) to directly interact with Yoda are provided in the following documents, which are maintained in a separate GitHub repository:

1. [Setting up VM](https://github.com/melanorian/bio_methods/blob/main/VM_set-up_Linux_VirtualBox.md)

2. [iRODS & iCommands](https://github.com/melanorian/bio_methods/blob/main/iCommands-for-YODA_iRODS.md)

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

- This step ensures that both file-level and collection-level information are aggregated for downstream analysis.
- JSON-formatted `file_types` allow flexible parsing and querying of file compositions per collection.
- The script ensures numeric consistency and accounts for corner cases where parent collection sizes are required.
