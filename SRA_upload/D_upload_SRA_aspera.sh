#!/bin/bash
#
# C_upload_retry_ascp.sh
#
# Retry an Aspera upload up to MAX_RETRIES times.
#
# Usage:
#   ./C_upload_retry_ascp.sh /path/to/local/upload_directory
#
# The NCBI destination and ascp command are defined below.
#
# --------------------------------------------------------------------

set -uo pipefail


# ---------------------- CONFIGURATION ----------------------

MAX_RETRIES=100

# Seconds to wait between retries
WAIT_SECONDS=60


# --------------------------------------------------------------------
# PASTE YOUR EXACT WORKING ASCP COMMAND BELOW
#
# Replace LOCAL_DIR with the variable "$UPLOAD_DIR"
#
# Example structure:
#
# ascp -i /path/to/key \
#      -QT \
#      -l100m \
#      -k1 \
#      -d \
#      "$UPLOAD_DIR" \
#      subascp@upload.ncbi.nlm.nih.gov:your_upload_destination
#
# --------------------------------------------------------------------

run_ascp_upload() {

    # >>> PASTE YOUR ASCP COMMAND HERE <<<
    
    ascp \
    -i /PATH/TO/YOUR/ASPERA_KEY \
    -QT \
    -l100m \
    -k1 \
    -d \
    "$UPLOAD_DIR" \
    subascp@upload.ncbi.nlm.nih.gov:YOUR_NCBI_UPLOAD_FOLDER

}


# ---------------------- ARGUMENT CHECK ----------------------

UPLOAD_DIR="${1:-}"

if [[ -z "$UPLOAD_DIR" ]]; then
    echo "Usage:"
    echo "  $0 /path/to/local/upload_directory"
    exit 1
fi


if [[ ! -d "$UPLOAD_DIR" ]]; then
    echo "ERROR: Directory does not exist:"
    echo "$UPLOAD_DIR"
    exit 1
fi


# ---------------------- LOG SETUP ----------------------

BASE_DIR="$(dirname "$UPLOAD_DIR")"
UPLOAD_NAME="$(basename "$UPLOAD_DIR")"

LOG_FILE="$BASE_DIR/upload_retry_${UPLOAD_NAME}.log"
ERR_FILE="$BASE_DIR/upload_retry_${UPLOAD_NAME}.stderr"

touch "$LOG_FILE"
touch "$ERR_FILE"


echo "====================================" | tee -a "$LOG_FILE"
echo "Aspera upload retry started" | tee -a "$LOG_FILE"
echo "Directory: $UPLOAD_DIR" | tee -a "$LOG_FILE"
echo "Maximum attempts: $MAX_RETRIES" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "====================================" | tee -a "$LOG_FILE"


# ---------------------- RETRY LOOP ----------------------

attempt=1

while [[ $attempt -le $MAX_RETRIES ]]
do

    echo "" | tee -a "$LOG_FILE"
    echo "------------------------------------" | tee -a "$LOG_FILE"
    echo "Attempt $attempt / $MAX_RETRIES" | tee -a "$LOG_FILE"
    echo "$(date)" | tee -a "$LOG_FILE"
    echo "------------------------------------" | tee -a "$LOG_FILE"


    # Run upload
    run_ascp_upload >>"$LOG_FILE" 2>>"$ERR_FILE"

    EXIT_CODE=$?


    if [[ $EXIT_CODE -eq 0 ]]; then

        echo "" | tee -a "$LOG_FILE"
        echo "====================================" | tee -a "$LOG_FILE"
        echo "UPLOAD SUCCESSFUL" | tee -a "$LOG_FILE"
        echo "Finished: $(date)" | tee -a "$LOG_FILE"
        echo "Attempts used: $attempt" | tee -a "$LOG_FILE"
        echo "====================================" | tee -a "$LOG_FILE"

        exit 0

    fi


    echo "Upload failed with exit code $EXIT_CODE" | tee -a "$LOG_FILE"


    # Basic detection of likely permanent failures
    if grep -Ei \
        "permission denied|authentication failed|invalid|not found|no such file|access denied" \
        "$ERR_FILE" >/dev/null
    then

        echo "" | tee -a "$LOG_FILE"
        echo "Permanent error detected. Stopping retry loop." | tee -a "$LOG_FILE"
        echo "Check:"
        echo "$ERR_FILE"

        exit $EXIT_CODE

    fi


    if [[ $attempt -lt $MAX_RETRIES ]]; then

        echo "Retrying in $WAIT_SECONDS seconds..." | tee -a "$LOG_FILE"
        sleep "$WAIT_SECONDS"

    fi


    attempt=$((attempt+1))

done


# ---------------------- FINAL FAILURE ----------------------

echo "" | tee -a "$LOG_FILE"
echo "====================================" | tee -a "$LOG_FILE"
echo "UPLOAD FAILED AFTER $MAX_RETRIES ATTEMPTS" | tee -a "$LOG_FILE"
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "See:"
echo "$LOG_FILE"
echo "$ERR_FILE"
echo "====================================" | tee -a "$LOG_FILE"


exit 1
