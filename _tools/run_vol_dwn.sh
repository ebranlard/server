#!/bin/bash
Delta=2
prev_vol=`amixer get PCM| grep -o [0-9]*%|sed 's/%//'`
new_vol=$(($prev_vol-$Delta))
echo "Vol down: $prev_vol% -> $new_vol%"
amixer set PCM -- $new_vol% > /dev/null
