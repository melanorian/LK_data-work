# LettuceKnow Support: Data Inventory & Organisation

The LettuceKnow consortium data are stored in the Yoda file management system. Yoda is based on iRODS, and interaction with its backend is possible via the iCommands suite.

Basic explanations of iRODS, relevant iCommands, and the setup of a virtual machine (VM) to directly interact with Yoda are provided in the following documents, which are maintained in a separate GitHub repository:

1. [Setting up VM](https://github.com/melanorian/bio_methods/blob/main/VM_set-up_Linux_VirtualBox.md)

2. [iRODS & iCommands](https://github.com/melanorian/bio_methods/blob/main/iCommands-for-YODA_iRODS.md)

## Workstream A: Inventory of Data on YODA 

[Bash script for collection-inventory]https://github.com/melanorian/LK_data-work/blob/main/inventory_yoda.sh

This script creates a **CSV inventory** of files in a Yoda/iRODS collection using `iquest`. It queries the iCAT catalog directly, making it efficient for large datasets.

### What it does

- Extracts file metadata:
  - Collection path (`COLL_NAME`)
  - File name (`DATA_NAME`)
  - File size in bytes (`DATA_SIZE`)
  - Replica number (`DATA_REPL_NUM`)
  - Checksum (`DATA_CHECKSUM`)
- Saves results to a CSV file  
- Writes a log file with execution details  
- Checks for errors and validates output  
- Reports total runtime  

### Input

- iRODS collection path inside the query (with `%` for recursion)  
- Active iRODS session (`iinit`)  

### Output

- CSV file: `./tiral_YODA_inventory/inventory_test.csv`  
- Log file: `./tiral_YODA_inventory/inventory_test.log`  

### Notes

- Uses `--no-page` for large outputs  
- File sizes are reported in **bytes**  
- Only accessible files are included  
