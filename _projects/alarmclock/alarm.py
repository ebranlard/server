#!/usr/bin/env python

import os.path
import pygame
import time
import configparser
# from time import gmtime, strftime
#  for time.sleep


# --------------------------------------------------------------------------------
# --- GLOBAL variables
# --------------------------------------------------------------------------------
FileTestSound='alarm_test_set'
FileAlarmSet='alarm_info_set'
FileAlarmInfo='alarm_info.txt'
FileLog='log.txt'

pygame.init()
clock = pygame.time.Clock();

class MusicFile:

#     def __init__(self,minv,maxv):

    def set_volume_range(self,minv,maxv):
        self.MinVolume=max(minv,0.01)
        self.MaxVolume=min(maxv,0.99)

    def play(self,filename,FadeTime=3000):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(self.MinVolume)
        clock = pygame.time.Clock();
        #pygame.mixer.music.play(fade_ms=3000)
        pygame.mixer.music.play()


        # ---Fade In
        nSteps=10;
        DeltaVolume=(self.MaxVolume-self.MinVolume)/float(nSteps)
        print(pygame.mixer.music.get_volume())
        print(DeltaVolume)
#         while pygame.mixer.get_busy() and pygame.mixer.music.get_volume()<0.9:
        volume=self.MinVolume;
        while volume<self.MaxVolume:
            volume=volume+DeltaVolume;
            pygame.mixer.music.set_volume(volume)
#             print(pygame.mixer.music.get_volume())
            clock.tick(FadeTime/nSteps)
            pygame.time.wait(FadeTime/nSteps)

    def fadeout(self,FadeTime):
        pygame.mixer.music.fadeout(FadeTime);
#         pygame.mixer.music.fadeout(3000)


def logit(info):
    fid=open(FileLog,'a')
    fid.write(info+'<br>\n')
    fid.close()
    print(info)

def loglast(info=""):
    if not info:
        # we open the log and get the last line
        with open(FileLog) as fid:
            last_line=list(fid)[-1]
    fid=open(FileLog,'w')
    fid.write(info+'\n')
    fid.close()


# --------------------------------------------------------------------------------
# --- Alarm
# --------------------------------------------------------------------------------
class Alarm:
    def __init__(self):
        self.reset();

    def reset(self):
        self.data=dict()

    def read(self):
        config = configparser.ConfigParser()
        config.read(FileAlarmInfo)
        self.data   = config["alarm_info"]
        self.data["Time"]=self.data["Time"].replace('"','')
        logit("Time  : "+ str(self.data["Time"]))
        logit("Volume: "+ str(self.data["Volume"]))

    def isTime(self):
        now=time.strftime("%H:%M", time.gmtime())
        try:
            return self.data["Time"]==now
        except:
            return False


    # --------------------------------------------------------------------------------
    # --- set alarm
    # --------------------------------------------------------------------------------
    def setFromFile(self):
        logit("Setting Alarm")
        self.read()
        loglast("Alarm set")

    # --------------------------------------------------------------------------------
    # ---Alarm
    # --------------------------------------------------------------------------------
    def now(self):
        logit("Launching alarm")
        volume=float(self.data["Volume"])
        print("Volume is ",volume)
        f = MusicFile()
        f.set_volume_range(volume*0.001,volume*1.1)
        f.play("Turkey Tree Call-SoundBible.com-1756787173.wav",3000)
        time.sleep(4)
        f.fadeout(1000);
        time.sleep(2)
        loglast("Done")

    # --------------------------------------------------------------------------------
    # ---
    # --------------------------------------------------------------------------------
    def test_sound_level(self):
        logit("Testing sound level")
        self.read()
        volume=float(self.data["Volume"])
        print("Volume is ",volume)
        f = MusicFile()
        f.set_volume_range(volume*0.001,volume*1.1)
    #     f.play("Sunny Day-SoundBible.com-2064222612.wav",3000)
        f.play("Turkey Tree Call-SoundBible.com-1756787173.wav",3000)
        time.sleep(1)
        f.fadeout(1000);
        time.sleep(2)
    #     # f.play("Swan.mp3")
        loglast("Test done")


# def main():

alarm=Alarm();

while True:
    # Testing sound level
    if os.path.isfile(FileTestSound):
        os.remove(FileTestSound);
        try:
            test_sound_level();
        except Exception as e:
            logit('ERROR')
            alarm.reset()
    # Setting alarm
    if os.path.isfile(FileAlarmSet):
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


    pygame.time.wait(1000)























