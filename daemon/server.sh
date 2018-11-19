#!/bin/sh

start() {
    echo "[START] Starting service" 
    MAINDIR=`dirname $(readlink -f $0)`
    echo "Daemon Dir: $MAINDIR"
    cd $MAINDIR
    python server.py
    #python server.py >> $LOGFILE 2>&1  
}

stop() {
    echo "[STOP] Stopping service" 
}

case $1 in
  start|stop) "$1" ;;
  *) 
      echo "usage: start, stop"
   ;;
esac

