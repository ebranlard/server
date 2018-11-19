#!/bin/bash

USER=manu
SERV=server

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

DATE=`date +"%Y%m%d-%H%M"`


# --------------------------------------------------------------------------------}
# --- Helper functions 
# --------------------------------------------------------------------------------{
lnbkp(){
    if [ -e $2 -o -h $2 ] ; then 
        echo "Backup of $2"
        mv $2 $2.bkp 
    fi
    echo "Symlink $2 -> $1"
    ln -s $1 $2
}



# ln -s /home/$USER/server
MAINDIR=`dirname $(readlink -f $0)`

echo "Main Directory: $MAINDIR"
echo "Date:           $DATE"
echo "User:           $USER"
echo "Servername:     $SERV"




lnbkp  $MAINDIR/_conf/$SERV.service /etc/systemd/system/$SERV.service 
lnbkp  $MAINDIR/_conf/$SERV.conf    /etc/rsyslog.d/$SERV.conf         

echo "- Enabling service"
systemctl enable $SERV

echo "- Starting service"
systemctl start $SERV
