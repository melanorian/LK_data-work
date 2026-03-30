# LettuceKnow Data Inventory & Organisation

The LettuceKnow consortium data are stored in the Yoda file management system. Yoda is based on iRODS, and interaction with its backend is possible via the iCommands suite.

Basic explanations of iRODS, relevant iCommands, and the setup of a virtual machine (VM) to directly interact with Yoda are provided in the following documents, which are maintained in a separate GitHub repository:

1. [Setting up VM](https://github.com/melanorian/bio_methods/blob/main/VM_set-up_Linux_VirtualBox.md)

2. [iRODS & iCommands](https://github.com/melanorian/bio_methods/blob/main/iCommands-for-YODA_iRODS.md)

## Workstream A: Inventory of Data on YODA 

### Step 1: [Bash script for collection-inventory](https://github.com/melanorian/LK_data-work/blob/main/inventory_yoda.sh)

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

### Step 2: [Python Processing Inventory CSVs & Generating Subcollection Summaries](https://github.com/melanorian/LK_data-work/blob/main/2_process_inventory_csv.py)

This Python workflow consolidates, cleans, and summarizes LettuceKnow inventory CSVs into hierarchical subcollection tables with aggregated file sizes.

**Input Variables**

- `BASE_DIR` – directory containing inventory CSVs (`inventory_<collection>/inventory.csv`)  
- `OUT_DIR` – output directory for subcollection summary CSV  
- `IGNORE_PRE` – path prefix to remove from file paths (optional)  
- `MAX_LEVEL` – depth of subcollection aggregation  

**Output**

- Combined, cleaned inventory table (`full_df` internally)  
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
