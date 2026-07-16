#!/bin/bash
#
# C_download_from_yoda_checksum_mismatch.sh
#
# Re-download only files that previously failed due to
# USER_CHKSUM_MISMATCH during iget -K.
#
# ---------------------------------------------------------------------------
# USAGE
#
#   ./C_download_from_yoda_checksum_mismatch.sh \
#       data_files/<experiment>/download_failed_<experiment>.log \
#       metadata/<experiment>_SRA_paths.csv
#
# Example:
#
#   ./C_download_from_yoda_checksum_mismatch.sh \
#       data_files/ExpMA001/download_failed_ExpMA001.log \
#       metadata/ExpMA001_SRA_paths.csv
#
# ARGUMENTS
#
#   1) download_failed_<experiment>.log
#        Log produced by download_from_yoda.sh
#
#   2) <experiment>_SRA_paths.csv
#        Original metadata CSV containing the file_path column.
#        Used for final verification that every expected file exists.
#
# OUTPUT
#
#   download_retry_success_<experiment>.log
#   download_retry_failed_<experiment>.log
#   download_missing_after_retry_<experiment>.log
#
# ---------------------------------------------------------------------------

set -euo pipefail

PARALLEL_JOBS=4

FAIL_LOG="${1:-}"
CSV_FILE="${2:-}"

if [[ -z "$FAIL_LOG" || -z "$CSV_FILE" ]]; then
    echo "Usage:"
    echo ""
    echo "  $0 download_failed_<experiment>.log <experiment>_SRA_paths.csv"
    echo ""
    exit 1
fi

if [[ ! -f "$FAIL_LOG" ]]; then
    echo "ERROR: Cannot find failure log:"
    echo "$FAIL_LOG"
    exit 1
fi

if [[ ! -f "$CSV_FILE" ]]; then
    echo "ERROR: Cannot find CSV:"
    echo "$CSV_FILE"
    exit 1
fi

# ------------------------------------------------------------
# Check iRODS session
# ------------------------------------------------------------

if ! ils >/dev/null 2>&1; then
    echo "ERROR: iRODS session not active."
    echo "Run iinit first."
    exit 1
fi

# ------------------------------------------------------------
# Output locations
# ------------------------------------------------------------

DIR="$(dirname "$FAIL_LOG")"

BASE="$(basename "$FAIL_LOG")"

EXPERIMENT="${BASE#download_failed_}"
EXPERIMENT="${EXPERIMENT%.log}"

SUCCESS2="$DIR/download_retry_success_${EXPERIMENT}.log"
FAIL2="$DIR/download_retry_failed_${EXPERIMENT}.log"
MISSING_LOG="$DIR/download_missing_after_retry_${EXPERIMENT}.log"

> "$SUCCESS2"
> "$FAIL2"
> "$MISSING_LOG"

TMP_LIST=$(mktemp)

# ------------------------------------------------------------
# Extract only checksum mismatch paths
# ------------------------------------------------------------

awk '

/USER_CHKSUM_MISMATCH/ {
    mismatch=1
    next
}

mismatch && /^\// {
    print
    mismatch=0
}

' "$FAIL_LOG" | sort -u > "$TMP_LIST"

TOTAL=$(wc -l < "$TMP_LIST")

echo ""
echo "======================================"
echo "Checksum mismatch retry"
echo "======================================"
echo "Experiment : $EXPERIMENT"
echo "Files to retry : $TOTAL"
echo "Parallel jobs : $PARALLEL_JOBS"
echo ""

if [[ "$TOTAL" -eq 0 ]]; then
    echo "No checksum mismatches detected."
    rm -f "$TMP_LIST"
    exit 0
fi

# ------------------------------------------------------------
# Retry download
# ------------------------------------------------------------

download_one() {

    local irods_path="$1"

    local filename
    filename=$(basename "$irods_path")

    local localfile="$DIR/$filename"

    echo "Retrying $filename"

    rm -f "$localfile"

    if iget -f -K "$irods_path" "$localfile" \
        >>"$SUCCESS2" 2>>"$FAIL2"
    then
        echo "$irods_path" >> "$SUCCESS2"
    else
        echo "$irods_path" >> "$FAIL2"
    fi
}

export -f download_one
export DIR SUCCESS2 FAIL2

cat "$TMP_LIST" |
xargs -P "$PARALLEL_JOBS" -I{} \
bash -c 'download_one "$@"' _ {}

rm -f "$TMP_LIST"

echo ""
echo "Retry download finished."
echo ""

# ------------------------------------------------------------
# Verification
# ------------------------------------------------------------

echo "Running full verification..."

HEADER=$(head -n 1 "$CSV_FILE")

PATH_COLUMN_INDEX=$(echo "$HEADER" |
tr ',' '\n' |
grep -nx "file_path" |
cut -d: -f1)

if [[ -z "$PATH_COLUMN_INDEX" ]]; then
    echo "ERROR: file_path column not found."
    exit 1
fi

EXPECTED_TOTAL=0

while IFS= read -r irods_path
do

    [[ -z "$irods_path" ]] && continue

    EXPECTED_TOTAL=$((EXPECTED_TOTAL+1))

    filename=$(basename "$irods_path")

    if ! find "$DIR" -type f -name "$filename" | grep -q .
    then
        echo "$irods_path" >> "$MISSING_LOG"
    fi

done < <(

tail -n +2 "$CSV_FILE" |
awk -F',' -v col="$PATH_COLUMN_INDEX" '
{
    gsub(/^[" ]+|[" ]+$/, "", $col)
    print $col
}
'

)

FOUND_TOTAL=$((EXPECTED_TOTAL - $(wc -l < "$MISSING_LOG")))
MISSING_TOTAL=$(wc -l < "$MISSING_LOG")

echo ""
echo "======================================"
echo "Verification summary"
echo "======================================"

echo "Expected files : $EXPECTED_TOTAL"
echo "Files found    : $FOUND_TOTAL"
echo "Missing files  : $MISSING_TOTAL"

echo ""
echo "Retry success log:"
echo "  $SUCCESS2"

echo ""
echo "Retry failure log:"
echo "  $FAIL2"

echo ""
echo "Missing log:"
echo "  $MISSING_LOG"

echo ""

if [[ "$MISSING_TOTAL" -eq 0 ]]; then
    echo "✓ All expected files are present."
else
    echo "⚠ $MISSING_TOTAL files are still missing."
fi
