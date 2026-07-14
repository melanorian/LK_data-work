#!/bin/bash

#

# download_from_yoda_add-seq.sh

#

# Download only add-seq files from a metadata CSV.

#

# Files are identified using:

# library_ID contains "_add-seq"

#

# Download source:

# file_path column

#

# Download destination:

# data_files/<experiment>/add_seq/

#

# Files are saved as:

# <library_ID>.fastq.gz

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
echo "Usage: $0 path/to/metadata.csv"
exit 1
fi

if [[ ! -f "$CSV_FILE" ]]; then
echo "ERROR: File not found: $CSV_FILE"
exit 1
fi

# ---- Derive experiment name and output folder ----

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

# ---- Check iCommands session ----

if ! ils >/dev/null 2>&1; then
echo "ERROR: iCommands session not active. Run 'iinit' first."
exit 1
fi

mkdir -p "$OUTPUT_DIR"

> "$SUCCESS_LOG"
> "$FAIL_LOG"
> "$MISSING_LOG"

HEADER=$(head -n 1 "$CSV_FILE")

LIBRARY_COLUMN_INDEX=$(echo "$HEADER" 
| tr "$DELIMITER" '\n' 
| grep -nx "$LIBRARY_COLUMN_NAME" 
| cut -d: -f1)

PATH_COLUMN_INDEX=$(echo "$HEADER" 
| tr "$DELIMITER" '\n' 
| grep -nx "$PATH_COLUMN_NAME" 
| cut -d: -f1)

if [[ -z "$LIBRARY_COLUMN_INDEX" ]]; then
echo "ERROR: Could not find column '$LIBRARY_COLUMN_NAME'"
exit 1
fi

if [[ -z "$PATH_COLUMN_INDEX" ]]; then
echo "ERROR: Could not find column '$PATH_COLUMN_NAME'"
exit 1
fi

echo "Using library_ID column index : $LIBRARY_COLUMN_INDEX"
echo "Using file_path column index  : $PATH_COLUMN_INDEX"
echo "Downloading to               : $OUTPUT_DIR"
echo "Parallel jobs                : $PARALLEL_JOBS"
echo ""

download_one() {

```
local library_id="$1"
local irods_path="$2"

local local_path="$OUTPUT_DIR/${library_id}.fastq.gz"

if [[ -f "$local_path" ]]; then
    echo "SKIP (already exists): $library_id" >> "$SUCCESS_LOG"
    return 0
fi

if iget -K "$irods_path" "$local_path" 2>>"$FAIL_LOG"; then
    echo "$library_id|$irods_path" >> "$SUCCESS_LOG"
else
    echo "$library_id|$irods_path" >> "$FAIL_LOG"
fi
```

}

export -f download_one
export OUTPUT_DIR SUCCESS_LOG FAIL_LOG

# ---- Download all add-seq files ----

tail -n +2 "$CSV_FILE" 
| awk -F"$DELIMITER" 
-v libcol="$LIBRARY_COLUMN_INDEX" 
-v pathcol="$PATH_COLUMN_INDEX" '
{
gsub(/^["\r ]+|["\r ]+$/, "", $libcol)
gsub(/^["\r ]+|["\r ]+$/, "", $pathcol)

```
if ($libcol ~ /_add-seq$/)
    print $libcol "\t" $pathcol
```

}' 
| xargs -P "$PARALLEL_JOBS" -d '\n' -I{} 
bash -c '
line="$1"
library_id=$(echo "$line" | cut -f1)
irods_path=$(echo "$line" | cut -f2-)

```
    download_one "$library_id" "$irods_path"
' _ {}
```

# ---- Verification pass ----

EXPECTED_COUNT=0
FOUND_COUNT=0

tail -n +2 "$CSV_FILE" 
| awk -F"$DELIMITER" 
-v libcol="$LIBRARY_COLUMN_INDEX" '
{
gsub(/^["\r ]+|["\r ]+$/, "", $libcol)

```
if ($libcol ~ /_add-seq$/)
    print $libcol
```

}' 
| while read -r LIBRARY_ID
do

```
EXPECTED_FILE="$OUTPUT_DIR/${LIBRARY_ID}.fastq.gz"

EXPECTED_COUNT=$((EXPECTED_COUNT + 1))

if [[ -f "$EXPECTED_FILE" ]]; then
    FOUND_COUNT=$((FOUND_COUNT + 1))
else
    echo "$LIBRARY_ID" >> "$MISSING_LOG"
fi
```

done

EXPECTED_TOTAL=$(tail -n +2 "$CSV_FILE" 
| awk -F"$DELIMITER" 
-v libcol="$LIBRARY_COLUMN_INDEX" '
{
gsub(/^["\r ]+|["\r ]+$/, "", $libcol)

```
if ($libcol ~ /_add-seq$/)
    count++
```

}
END {
print count
}')

FOUND_TOTAL=$(find "$OUTPUT_DIR" 
-maxdepth 1 
-name "*_add-seq.fastq.gz" 
| wc -l)

MISSING_TOTAL=$(wc -l < "$MISSING_LOG")

echo ""
echo "Verification complete."
echo ""
echo "Expected add-seq files : $EXPECTED_TOTAL"
echo "Files present          : $FOUND_TOTAL"
echo "Missing files          : $MISSING_TOTAL"
echo ""
echo "Success log : $SUCCESS_LOG"
echo "Failure log : $FAIL_LOG"
echo "Missing log : $MISSING_LOG"
echo ""
echo "Done."
