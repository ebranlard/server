#!/bin/bash

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


MAINDIR=`dirname $(readlink -f $0)`

echo "Main Directory: $MAINDIR"

# TODO check nginx installed

lnbkp  $MAINDIR/nginx.conf     /etc/nginx/nginx.conf
lnbkp  $MAINDIR/serversite     /etc/nginx/sites-available/serversite

cd /etc/nginx/sites-enabled
rm -f serversite 
ln -s ../sites-available/serversite serversite
