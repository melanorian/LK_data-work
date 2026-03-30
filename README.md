# LettuceKnow Data Inventory & Organisation

The LettuceKnow consortium data are stored in the Yoda file management system. Yoda is based on iRODS, and interaction with its backend is possible via the iCommands suite.

Basic explanations of iRODS, relevant iCommands, and the setup of a virtual machine (VM) to directly interact with Yoda are provided in the following documents, which are maintained in a separate GitHub repository:

1. [Setting up VM](https://github.com/melanorian/bio_methods/blob/main/VM_set-up_Linux_VirtualBox.md)

2. [iRODS & iCommands](https://github.com/melanorian/bio_methods/blob/main/iCommands-for-YODA_iRODS.md)

## Workstream A: Inventory of Data on YODA 

### Step 1: [Bash script for collection-inventory](https://github.com/melanorian/LK_data-work/blob/main/inventory_yoda.sh)

This script creates a **CSV inventory** of files in a Yoda/iRODS collection using `iquest`. It queries the iCAT catalog directly, making it efficient for large datasets.

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

**Input**

- iRODS collection path (configured in `base_collection`)
- Active iRODS session (`iinit`)  
- Optional: uncomment alternate query to include `DATA_CREATE_TIME`

**Output**

- CSV file: `./inventory_<basename of collection>/inventory.csv`  
- Log file: `./inventory_<basename of collection>/inventory.log`  

## Configuration (edit only these)

- `base_collection` - path to the iRODS collection you want to inventory
- Header, format, and query lines - Default with creation time (comment to deactivate with "#"), alternative: without creation time (uncomment to activate removing "#")

### Notes

- iRODS DATA_CREATE_TIME is returned as a Unix timestamp-like integer - requires downstream conversion. E.g. 01727370936 == Thu Sep 26 2024 19:15:36 GMT+0200 (Central European Summer Time)
- File sizes are reported in **bytes**  
- Only accessible files can be included
