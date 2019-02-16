#!/bin/bash
# requirements:
#  apt-get install samba samba-common


USER=manu
SERV=server

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi



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


# --------------------------------------------------------------------------------}
# --- Main setup
# --------------------------------------------------------------------------------{
MAINDIR=`dirname $(readlink -f $0)`

echo "Main Directory: $MAINDIR"
echo "Date:           $DATE"
echo "User:           $USER"




lnbkp  $MAINDIR/_conf/smb.conf /etc/samba/smb.conf

sudo smbpasswd -a $USER

sudo service smbd restart
