#!/usr/bin/env python

import socket
import sys
from datetime import datetime
import os
import os.path
import time


#from alarm import Alarm, FileTestSound, FileAlarmSet, FileAlarmInfo, logit
#alarm=Alarm();


#PID = os.getpid()
UDP_IP = "127.0.0.1"
UDP_PORT = 5005


def log(s):
    #print(datetime.now().strftime('[%Y/%m/%d-%H:%M] ')+'['+str(PID)+'] '+s)
    print(s)
    sys.stdout.flush()


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    sock.bind((UDP_IP, UDP_PORT))
except Exception as e:
    log('=== Server already running')
    sys.exit(-1)

log('>>> Server started')
try:
    log('Socket created')

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        data = data.strip()
        log('Received: '+data.strip())
        # Music Stop
        if data == 'MusicStop':
            log('>Server: Music Stop')
            os.system('killall vlc')
        # Music Start
        if data == 'MusicStart':
            log('>Server: Signal Music Start')
            os.system('killall vlc') # to avoid cacophony
            os.system('/home/manu/server/daemon/run_music.sh')
        # Volume Up
        if data == 'VolUp':
            log('>Server: Signal Music Up')
            os.system('/www/site/run_vol_up.sh')
        # Volume Down
        if data == 'VolDown':
            log('>Server: Signal Music Down')
            os.system('/www/site/run_vol_dwn.sh')
        # Alarm test
        #if data == 'AlarmTest':
        #    alarm.test_sound_level();
    sys.exit(0)

except Exception as e:
    #log('Exception: '+str(e.args[0])+e.strerror)
    log('Exception: '+str(e.strerror))
    log('<<< Server stopped')
    sys.exit(-1)

