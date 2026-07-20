#!/bin/bash
#
# C_upload_retry_ascp.sh
#
# Retry an Aspera upload up to MAX_RETRIES times.
#
# Usage:
#
# bash C_upload_retry_ascp.sh \
#     /path/to/aspera_key \
#     /path/to/local_upload_directory \
#     subasp@upload.ncbi.nlm.nih.gov:upload_destination
#
# --------------------------------------------------------------------

set -uo pipefail


# ---------------------- CONFIGURATION ----------------------

MAX_RETRIES=100

# Seconds to wait between retries
WAIT_SECONDS=60


# ---------------------- ARGUMENT CHECK ----------------------

ASPERA_KEY="${1:-}"
UPLOAD_DIR="${2:-}"
NCBI_DEST="${3:-}"


if [[ -z "$ASPERA_KEY" || -z "$UPLOAD_DIR" || -z "$NCBI_DEST" ]]; then

    echo ""
    echo "Usage:"
    echo ""
    echo "  $0 <aspera_key> <local_upload_directory> <ncbi_destination>"
    echo ""
    echo "Example:"
    echo ""
    echo "  $0 ~/keys/aspera.openssh \\"
    echo "     data_files/LKAtlasRNAseq001_A \\"
    echo "     subasp@upload.ncbi.nlm.nih.gov"
    echo ""

    exit 1
fi


if [[ ! -f "$ASPERA_KEY" ]]; then
    echo "ERROR: Aspera key not found:"
    echo "$ASPERA_KEY"
    exit 1
fi


if [[ ! -d "$UPLOAD_DIR" ]]; then
    echo "ERROR: Upload directory not found:"
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
echo "" | tee -a "$LOG_FILE"
echo "Upload directory:" | tee -a "$LOG_FILE"
echo "$UPLOAD_DIR" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "NCBI destination:" | tee -a "$LOG_FILE"
echo "$NCBI_DEST" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Maximum attempts: $MAX_RETRIES" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "====================================" | tee -a "$LOG_FILE"



# ---------------------- ASCP FUNCTION ----------------------

run_ascp_upload() {

    ~/.aspera/connect/bin/ascp \
        -i "$ASPERA_KEY" \
        -QT \
        -l100m \
        -k1 \
        -d \
        "$UPLOAD_DIR" \
        "$NCBI_DEST"

}



# ---------------------- RETRY LOOP ----------------------

attempt=1


while [[ $attempt -le $MAX_RETRIES ]]
do

    echo "" | tee -a "$LOG_FILE"
    echo "------------------------------------" | tee -a "$LOG_FILE"
    echo "Attempt $attempt / $MAX_RETRIES" | tee -a "$LOG_FILE"
    echo "$(date)" | tee -a "$LOG_FILE"
    echo "------------------------------------" | tee -a "$LOG_FILE"


    #
    # Run Aspera:
    # - show output live
    # - save output to log
    # - save errors separately
    #

    stdbuf -oL run_ascp_upload \
        2> >(tee -a "$ERR_FILE" >&2) \
        | tee -a "$LOG_FILE"


    EXIT_CODE=${PIPESTATUS[0]}



    if [[ $EXIT_CODE -eq 0 ]]; then

        echo "" | tee -a "$LOG_FILE"
        echo "====================================" | tee -a "$LOG_FILE"
        echo "UPLOAD SUCCESSFUL" | tee -a "$LOG_FILE"
        echo "Finished: $(date)" | tee -a "$LOG_FILE"
        echo "Attempts used: $attempt" | tee -a "$LOG_FILE"
        echo "====================================" | tee -a "$LOG_FILE"

        exit 0

    fi



    echo "" | tee -a "$LOG_FILE"
    echo "Upload failed with exit code $EXIT_CODE" | tee -a "$LOG_FILE"



    # ---------------- Permanent error detection ----------------

    if grep -Ei \
        "permission denied|authentication failed|invalid|not found|no such file|access denied|authorization" \
        "$ERR_FILE" >/dev/null
    then

        echo "" | tee -a "$LOG_FILE"
        echo "Permanent error detected." | tee -a "$LOG_FILE"
        echo "Stopping retry loop." | tee -a "$LOG_FILE"
        echo "See:"
        echo "$ERR_FILE"

        exit "$EXIT_CODE"

    fi



    # ---------------- Retry wait ----------------

    if [[ $attempt -lt $MAX_RETRIES ]]; then

        echo "" | tee -a "$LOG_FILE"
        echo "Temporary failure detected." | tee -a "$LOG_FILE"
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
echo "" | tee -a "$LOG_FILE"
echo "Log file:"
echo "$LOG_FILE"
echo ""
echo "Error file:"
echo "$ERR_FILE"
echo "====================================" | tee -a "$LOG_FILE"


exit 1
