#!/usr/bin/env python
from alarm import Alarm, FileTestSound, FileAlarmSet, FileAlarmInfo, logit

import os
import os.path
import time

alarm=Alarm();


FileMusicStop ='/www/site/_listen/music_stop'
FileMusicStart='/www/site/_listen/music_start'
FileMusicUp   ='/www/site/_listen/music_up'
FileMusicDown ='/www/site/_listen/music_down'


print('>Server: Start');

while True:
    # Music Stop
    if os.path.isfile(FileMusicStop):
        print('>Server: Music Stop')
        os.remove(FileMusicStop);
        os.system('killall vlc')

    # Music Start
    if os.path.isfile(FileMusicStart):
        print('>Server: Signal Music Start')
        os.remove(FileMusicStart);
        os.system('killall vlc') # to avoid cacophony
        os.system('/www/site/run_music.sh')

    # Volume Up
    if os.path.isfile(FileMusicUp):
        print('>Server: Signal Music Up')
        os.remove(FileMusicUp);
        os.system('/www/site/run_vol_up.sh')
    # Volume Down
    if os.path.isfile(FileMusicDown):
        print('>Server: Signal Music Down')
        os.remove(FileMusicDown);
        os.system('/www/site/run_vol_dwn.sh')

    # Testing sound level
    if os.path.isfile(FileTestSound):
        print('>Server: Signal Test Sound')
        os.remove(FileTestSound);
        try:
            alarm.test_sound_level();
        except Exception as e:
            logit('ERROR')
            alarm.reset()
    # Setting alarm
    if os.path.isfile(FileAlarmSet):
        print('>Server: Signal Setting alarm')
        os.remove(FileAlarmSet);
        try:
            alarm.setFromFile()
        except Exception as e:
            logit('ERROR')
            alarm.reset()
    # Launching alarm
    if alarm.isTime():
#         try:
        alarm.now();
#         except Exception as e:
#             logit('ERROR')
#             alarm.reset()


    time.sleep(0.1)























