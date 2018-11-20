#!/bin/bash

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
cpbkp(){
    if [ -e $2 ] ; then 
        echo "Backup of $2"
        mv $2 $2.bkp 
    fi
    ln $1 $2
}


MAINDIR=`dirname $(readlink -f $0)`

echo "Main Directory: $MAINDIR"

lnbkp  $MAINDIR/dhcpcd.conf   /etc/dhcpcd.conf
lnbkp  $MAINDIR/dnsmasq.conf  /etc/dnsmasq.conf
lnbkp  $MAINDIR/hostapd       /etc/default/hostapd

cpbkp $MAINDIR/hostapd.conf.editme /etc/hostapd/hostapd.conf

echo ">>> You need to edit /etc/hostapd/hostapd.conf with the proper SSID and PASSPHRASE"

# TODO iptables
