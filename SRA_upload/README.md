Run script form the terminal and doesn't stop the process if the terminal gets closed to prevent interruption of large download

`nohup ./download_from_yoda.sh ExpXYZ_SRA_paths.csv > run.log 2>&1 &` 

inspect progress: 

`tail -f run.log` 
