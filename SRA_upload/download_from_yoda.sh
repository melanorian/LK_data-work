#!/bin/bash
#
# download_from_yoda.sh
#
# Bulk-download files from Yoda (iRODS) based on a list of paths in a CSV file.
# Designed for large batches (e.g. thousands of RNAseq samples) with logging,
# resume support, and optional parallel downloads.
#
# ---------------------------------------------------------------------------
# USAGE
#   ./download_from_yoda.sh path/to/samples.csv
#
# REQUIREMENTS
#   - iCommands installed and iinit already run successfully (valid session)
#   - CSV file with a header row, containing a column of full iRODS paths
#     e.g.  sample_id,irods_path
#           sample001,/nluu6p/home/research-myproject/sample001.fastq.gz
#           sample002,/nluu6p/home/research-myproject/sample002.fastq.gz
#
#   If your Excel sheet has full paths in a differently-named column, just
#   change PATH_COLUMN_NAME below, or change PATH_COLUMN_INDEX if you'd
#   rather reference the column by number (1-indexed).
#
# ---------------------------------------------------------------------------

set -uo pipefail

# ---------------------- CONFIGURATION (edit as needed) ----------------------

# Name of the column in the CSV that contains the full iRODS path to each file.
# Leave blank and set PATH_COLUMN_INDEX instead if you prefer to reference by
# column number.
PATH_COLUMN_NAME="file_path"
PATH_COLUMN_INDEX=""   # e.g. "2" for the 2nd column; leave blank to use name above

# CSV delimiter - your *_SRA_paths.csv files are comma-delimited
DELIMITER=","

# Local folder where files will be downloaded to.
#
# By default this is auto-computed as:
#   <parent of script's folder>/data_files/<experiment_name>/
# where <experiment_name> is derived from the CSV filename by stripping
# "_SRA_paths.csv" (e.g. "ExpMA002_SRA_paths.csv" -> "ExpMA002").
#
# This assumes the script lives in a "script" folder that is a sibling of
# "data_files" and "metadata", e.g.:
#   RNAseq_submission_LK/
#     data_files/
#     metadata/
#     script/download_from_yoda.sh
#
# You can still override it manually if needed, e.g.:
#   OUTPUT_DIR="/some/other/place" ./download_from_yoda.sh samples.csv
OUTPUT_DIR_OVERRIDE="${OUTPUT_DIR:-}"

# How many parallel downloads to run at once.
# Start conservative (4-8); too high can overwhelm the server or your network.
PARALLEL_JOBS=4

# ------------------------------------------------------------------------

CSV_FILE="${1:-}"

if [[ -z "$CSV_FILE" ]]; then
    echo "Usage: $0 path/to/samples.csv"
    exit 1
fi

if [[ ! -f "$CSV_FILE" ]]; then
    echo "ERROR: File not found: $CSV_FILE"
    exit 1
fi

# ---- Derive experiment name and output folder ----

# Directory this script itself lives in (e.g. .../RNAseq_submission_LK/script)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# One level up (e.g. .../RNAseq_submission_LK)
SUBMISSION_DIR="$(dirname "$SCRIPT_DIR")"

# Experiment name = CSV filename with "_SRA_paths.csv" stripped
CSV_BASENAME="$(basename "$CSV_FILE")"
EXPERIMENT_NAME="${CSV_BASENAME%_SRA_paths.csv}"

if [[ -n "$OUTPUT_DIR_OVERRIDE" ]]; then
    OUTPUT_DIR="$OUTPUT_DIR_OVERRIDE"
else
    OUTPUT_DIR="$SUBMISSION_DIR/data_files/$EXPERIMENT_NAME"
fi

# Keep logs alongside the downloaded data, tagged with experiment name
# so re-running for a different experiment doesn't overwrite previous logs.
SUCCESS_LOG="$OUTPUT_DIR/download_success_${EXPERIMENT_NAME}.log"
FAIL_LOG="$OUTPUT_DIR/download_failed_${EXPERIMENT_NAME}.log"

# Check iCommands session is active
if ! ils >/dev/null 2>&1; then
    echo "ERROR: iCommands session not active. Run 'iinit' first (or your PAM password may have expired)."
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
> "$SUCCESS_LOG"
> "$FAIL_LOG"

# Determine which column index to use
HEADER=$(head -n 1 "$CSV_FILE")

if [[ -z "$PATH_COLUMN_INDEX" ]]; then
    PATH_COLUMN_INDEX=$(echo "$HEADER" | tr "$DELIMITER" '\n' | grep -nx "$PATH_COLUMN_NAME" | cut -d: -f1)
    if [[ -z "$PATH_COLUMN_INDEX" ]]; then
        echo "ERROR: Could not find column '$PATH_COLUMN_NAME' in header: $HEADER"
        echo "Either fix PATH_COLUMN_NAME, or set PATH_COLUMN_INDEX manually."
        exit 1
    fi
fi

echo "Using column index $PATH_COLUMN_INDEX for iRODS paths."
echo "Downloading to: $OUTPUT_DIR"
echo "Parallel jobs: $PARALLEL_JOBS"
echo ""

# Function that downloads a single file
download_one() {
    local irods_path="$1"
    local filename
    filename=$(basename "$irods_path")
    local local_path="$OUTPUT_DIR/$filename"

    # Skip if already downloaded
    if [[ -f "$local_path" ]]; then
        echo "SKIP (already exists): $irods_path" >> "$SUCCESS_LOG"
        return 0
    fi

    # -f  : force overwrite if partially there
    # -K  : verify checksum after transfer
    if iget -K "$irods_path" "$local_path" 2>>"$FAIL_LOG"; then
        echo "$irods_path" >> "$SUCCESS_LOG"
    else
        echo "$irods_path" >> "$FAIL_LOG"
    fi
}
export -f download_one
export OUTPUT_DIR SUCCESS_LOG FAIL_LOG

# Extract paths (skip header), strip quotes/whitespace, and run downloads
tail -n +2 "$CSV_FILE" \
    | awk -F"$DELIMITER" -v col="$PATH_COLUMN_INDEX" '{gsub(/^["\r ]+|["\r ]+$/,"",$col); print $col}' \
    | grep -v '^\s*$' \
    | xargs -P "$PARALLEL_JOBS" -I{} bash -c 'download_one "$@"' _ {}

echo ""
echo "Done."
echo "  Successful: $(wc -l < "$SUCCESS_LOG")"
echo "  Failed:     $(wc -l < "$FAIL_LOG")"
echo ""
echo "Failed paths (if any) are listed in $FAIL_LOG - you can copy them into"
echo "a new CSV and re-run this script to retry just those."
