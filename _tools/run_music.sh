#!/bin/bash

echo "Running music (log: vlc_log.txt)"
#runuser -l manu -c 'cvlc --random /home/manu/Music/Decouverte2/&'  &> /www/site/_data/vlc_log.txt 
cvlc --random /home/manu/Music/Decouverte2/   &
# &> /home/manu/server/daemon/vlc_log.txt &

