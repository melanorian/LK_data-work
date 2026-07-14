#!/bin/bash
#
# download_from_yoda_add-seq.sh
#
# Download add-seq FASTQ files from Yoda based on metadata CSV.
#
# Required CSV columns:
#   library_ID
#   file_path
#
# Add-seq files are identified by:
#   library_ID containing "_add-seq"
#
# Files are saved as:
#   <library_ID>.fastq.gz
#
# ---------------------------------------------------------------------------

set -uo pipefail


# ---------------------- CONFIGURATION ----------------------

LIBRARY_COLUMN_NAME="library_ID"
PATH_COLUMN_NAME="file_path"

DELIMITER=","

OUTPUT_DIR_OVERRIDE="${OUTPUT_DIR:-}"

PARALLEL_JOBS=4

# -----------------------------------------------------------


CSV_FILE="${1:-}"

if [[ -z "$CSV_FILE" ]]; then
    echo "Usage:"
    echo "$0 path/to/metadata.csv"
    exit 1
fi

if [[ ! -f "$CSV_FILE" ]]; then
    echo "ERROR: File not found: $CSV_FILE"
    exit 1
fi


# ---------------------- DIRECTORIES -------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBMISSION_DIR="$(dirname "$SCRIPT_DIR")"

CSV_BASENAME="$(basename "$CSV_FILE")"
EXPERIMENT_NAME="${CSV_BASENAME%_SRA_paths.csv}"


if [[ -n "$OUTPUT_DIR_OVERRIDE" ]]; then
    OUTPUT_DIR="$OUTPUT_DIR_OVERRIDE/add_seq"
else
    OUTPUT_DIR="$SUBMISSION_DIR/data_files/$EXPERIMENT_NAME/add_seq"
fi


SUCCESS_LOG="$OUTPUT_DIR/download_success_add_seq_${EXPERIMENT_NAME}.log"
FAIL_LOG="$OUTPUT_DIR/download_failed_add_seq_${EXPERIMENT_NAME}.log"
MISSING_LOG="$OUTPUT_DIR/missing_add_seq_${EXPERIMENT_NAME}.log"


# ---------------------- CHECK YODA --------------------------

if ! ils >/dev/null 2>&1; then
    echo "ERROR: iRODS session not active."
    echo "Run iinit first."
    exit 1
fi


mkdir -p "$OUTPUT_DIR"

> "$SUCCESS_LOG"
> "$FAIL_LOG"
> "$MISSING_LOG"


# ---------------------- FIND COLUMNS ------------------------

HEADER=$(head -n 1 "$CSV_FILE")


LIBRARY_COLUMN_INDEX=$(echo "$HEADER" | tr "$DELIMITER" '\n' | grep -nx "$LIBRARY_COLUMN_NAME" | cut -d: -f1)

PATH_COLUMN_INDEX=$(echo "$HEADER" | tr "$DELIMITER" '\n' | grep -nx "$PATH_COLUMN_NAME" | cut -d: -f1)


if [[ -z "$LIBRARY_COLUMN_INDEX" ]]; then
    echo "ERROR: Could not find column $LIBRARY_COLUMN_NAME"
    exit 1
fi


if [[ -z "$PATH_COLUMN_INDEX" ]]; then
    echo "ERROR: Could not find column $PATH_COLUMN_NAME"
    exit 1
fi


echo "Experiment: $EXPERIMENT_NAME"
echo "Library column: $LIBRARY_COLUMN_INDEX"
echo "Path column: $PATH_COLUMN_INDEX"
echo "Output directory: $OUTPUT_DIR"
echo "Parallel jobs: $PARALLEL_JOBS"
echo ""


# ---------------------- DOWNLOAD FUNCTION -------------------

download_one()
{
    local library_id="$1"
    local irods_path="$2"

    local filename="${library_id}.fastq.gz"
    local local_path="$OUTPUT_DIR/$filename"


    if [[ -f "$local_path" ]]; then
        echo "SKIP: $filename" >> "$SUCCESS_LOG"
        return 0
    fi


    if iget -K "$irods_path" "$local_path" 2>>"$FAIL_LOG"; then
        echo "$filename|$irods_path" >> "$SUCCESS_LOG"
    else
        echo "$filename|$irods_path" >> "$FAIL_LOG"
    fi
}


export -f download_one
export OUTPUT_DIR SUCCESS_LOG FAIL_LOG


# ---------------------- DOWNLOAD ADD-SEQ FILES --------------

tail -n +2 "$CSV_FILE" |
awk -F"$DELIMITER" \
-v libcol="$LIBRARY_COLUMN_INDEX" \
-v pathcol="$PATH_COLUMN_INDEX" '
{
    gsub(/^[" ]+|[" ]+$/, "", $libcol)
    gsub(/^[" ]+|[" ]+$/, "", $pathcol)

    if ($libcol ~ /_add-seq$/)
        print $libcol "\t" $pathcol
}' |
while IFS=$'\t' read -r library_id irods_path
do
    echo "$library_id|$irods_path"
done |
xargs -P "$PARALLEL_JOBS" -I{} bash -c '
    library_id="${1%%|*}"
    irods_path="${1#*|}"
    download_one "$library_id" "$irods_path"
' _ {}


# ---------------------- VERIFICATION ------------------------

echo ""
echo "Running verification..."


EXPECTED_TOTAL=0
FOUND_TOTAL=0


tail -n +2 "$CSV_FILE" |
awk -F"$DELIMITER" \
-v libcol="$LIBRARY_COLUMN_INDEX" '
{
    gsub(/^[" ]+|[" ]+$/, "", $libcol)

    if ($libcol ~ /_add-seq$/)
        print $libcol
}' |
while read -r library_id
do

    EXPECTED_TOTAL=$((EXPECTED_TOTAL+1))

    expected_file="$OUTPUT_DIR/${library_id}.fastq.gz"

    if [[ -f "$expected_file" ]]; then
        FOUND_TOTAL=$((FOUND_TOTAL+1))
    else
        echo "$library_id" >> "$MISSING_LOG"
    fi

done


EXPECTED_TOTAL=$(grep -c "_add-seq" "$CSV_FILE" || true)

FOUND_TOTAL=$(find "$OUTPUT_DIR" -maxdepth 1 -name "*_add-seq.fastq.gz" | wc -l)

MISSING_TOTAL=$(wc -l < "$MISSING_LOG")


echo ""
echo "=============================="
echo "Verification summary"
echo "=============================="
echo "Expected add-seq files : $EXPECTED_TOTAL"
echo "Downloaded files       : $FOUND_TOTAL"
echo "Missing files          : $MISSING_TOTAL"
echo ""
echo "Success log:"
echo "$SUCCESS_LOG"
echo ""
echo "Failure log:"
echo "$FAIL_LOG"
echo ""
echo "Missing log:"
echo "$MISSING_LOG"
echo ""

echo "Done."