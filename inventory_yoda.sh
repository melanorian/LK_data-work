#!/bin/bash

# Start timer
start_time=$(date +%s)

# Create output directory if it doesn’t exist
mkdir -p ./tiral_YODA_inventory

# Log file
logfile=./tiral_YODA_inventory/inventory_test.log
echo "Starting inventory script at $(date)" > "$logfile"

# Write header to CSV
echo "COLL_NAME,DATA_NAME,DATA_SIZE,DATA_REPL_NUM,DATA_CHECKSUM" > ./tiral_YODA_inventory/inventory_test.csv

# Append iquest output in CSV format, log stdout/stderr
iquest --no-page "%s/%s,%s,%s,%s" "select COLL_NAME, DATA_NAME, DATA_SIZE, DATA_REPL_NUM, DATA_CHECKSUM where COLL_NAME like '/nluu6p/home/research-lettuceknow-releases/1_data-releases/data-release_V2_20241031/3_results%'" >

# Check if iquest finished successfully
if [ $? -eq 0 ]; then
    echo "iquest command finished successfully." >> "$logfile"
else
    echo "ERROR: iquest command failed!" >> "$logfile"
    echo "Check $logfile for details."
    exit 1
fi

# Check if CSV is non-empty (after header)
if [ $(wc -l < ./tiral_YODA_inventory/inventory_test.csv) -le 1 ]; then
    echo "ERROR: CSV file is empty!" >> "$logfile"
    echo "Check $logfile for details."
    exit 1
fi

# End timer and print runtime
end_time=$(date +%s)
runtime=$((end_time - start_time))
echo "Script finished successfully in $runtime seconds." >> "$logfile"
echo "Inventory CSV saved to ./tiral_YODA_inventory/inventory_test.csv"
