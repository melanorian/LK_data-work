#!/bin/bash

set -o pipefail  # catch failures in pipes

# start timer
start_time=$(date +%s)

## configuration

# base collection (edit this only)
base_collection="/nluu6p/home/research-lettuceknow-releases"

# output directory derived from collection name
outdir="./inventory_$(basename "$base_collection")"
mkdir -p "$outdir"

# log and csv files
logfile="$outdir/inventory.log"
csvfile="$outdir/inventory.csv"

# header, format, query
# default: without creation time
# header="COLL_NAME/DATA_NAME,DATA_SIZE,DATA_REPL_NUM,DATA_CHECKSUM"
# format="%s/%s,%s,%s,%s"
# query="select COLL_NAME, DATA_NAME, DATA_SIZE, DATA_REPL_NUM, DATA_CHECKSUM where COLL_NAME like '${base_collection}%'"

# alternative: with creation time (uncomment to use)
header="COLL_NAME,DATA_NAME,DATA_SIZE,DATA_REPL_NUM,DATA_CHECKSUM,DATA_CREATE_TIME"
format="%s/%s,%s,%s,%s,%s"
query="select COLL_NAME, DATA_NAME, DATA_SIZE, DATA_REPL_NUM, DATA_CHECKSUM, DATA_CREATE_TIME where COLL_NAME like '${base_collection}%'"

## log configuration

echo "Starting inventory script at $(date)" > "$logfile"
echo "Base collection: $base_collection" >> "$logfile"
echo "Output directory: $outdir" >> "$logfile"
echo "Header: $header" >> "$logfile"
echo "Format: $format" >> "$logfile"
echo "Query: $query" >> "$logfile"

## write header
echo "$header" > "$csvfile"

## run iquest (safe execution)
if iquest --no-page "$format" "$query" >> "$csvfile" 2>> "$logfile"; then
    echo "iquest command finished successfully" >> "$logfile"
else
    echo "ERROR: iquest command failed" >> "$logfile"
    exit 1
fi

## count rows
row_count=$(wc -l < "$csvfile")
data_rows=$((row_count - 1))

echo "Total rows (incl header): $row_count" >> "$logfile"
echo "Data rows: $data_rows" >> "$logfile"

if [ "$row_count" -le 1 ]; then
    echo "ERROR: CSV file is empty" >> "$logfile"
    exit 1
fi

## end timer
end_time=$(date +%s)
runtime=$((end_time - start_time))

echo "Finished in $runtime seconds" >> "$logfile"
echo "Inventory CSV saved to $csvfile"