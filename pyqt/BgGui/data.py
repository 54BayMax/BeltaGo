# -*- coding: utf-8 -*-

from voiceTxt import * 
import threading
import os
class data:
    def __init__(self):
        self.obj=True
        self.color=['33FF00','40FF00','51FF00','5AFF00','62FF00','6FFF00','77FF00','89FF00','95FF00','9EFF00',
       'ABFF00','AFFF00','B3FF00','BCFF00','C4FF00','CDFF00','D1FF00','D5FF00','DAFF00','E2FF00',
       'EBFF00','EFFF00','F3FF00','FFFF00','FFF300','FFEF00','FFEB00','FFE600','FFDE00','FFDA00',
       'FFD100','FFC900','FFC400','FFBC00','FFB300','FFA600','FFA200','FF9500','FF8D00','FF8000',
       'FF7C00','FF7300','FF6B00','FF6600','FF5E00','FF5500','FF5100','FF4400','FF3700','FF2F00',
       'FF2B00','FF1E00','FF1500','FF0900','FF0400','FF0000']
        self.SpeakRate = 10
        self.SpeakPitch = 70
        self.SpeakVolume = 0
        self.SpeakLock = False
        
    def speak(self, words):
        global SpeakLock
        if  self.SpeakLock:
            self.SpeakLock = True
            t = threading.Thread(target=self.Thread_Speak, args = (words, ))
            t.start()
    def Thread_Speak(self, words):
        os.system(u'ekho "%s" -p %d -r %d -a %d'%(words,self.SpeakPitch, self.SpeakRate, self.SpeakVolume))
        self.SpeakLock=False
        
    def slider_data(self,value):
        return u'<font color="#%s"><b>速度:%d</b></font>'%(self.color[value],value)
    def setobj(self,obj):
        self.obj=obj
    def button_data(self,str,flag=False):
        if not flag:
            return u'<font color="#086290"><b>%s</b></font>'%str
        else:
            return u'<font color="#FF0000"><b>%s</b></font>'%str
    def normal_data(self, str,flag=True):
        if flag:
            return u'<font color="#08900C"><b>%s</b></font>'%str
        else:
            return u'<p  align="right"><font color="#08900C"><b>%s</b></font><\p>'%str
    
    def dealWithData(self, data, speed, dir, servo):
        for l in Llist:
            if l in data:
                dir='L'
        for r in Rlist:
            if r in data:
                dir='R'
        for u in Ulist:
            if u in data:
                dir='U'
        for d in Dlist:
            if d in data:
                dir='D'
        for h in Hlist:
            if h in data:
                dir='H'
        for UServo in UpServoList:
            if UServo in data:
                servo = 0
        for DServo in DownServoList:
            if DServo in data:
                servo = 1
        for USpeed in SpeedUpList:
            if USpeed in data:
                speed = speed + 9
                if speed >= 55:
                    speed = 55
                    self.speak('我已使出洪荒之力啦')
        for DSpeed in SpeedDownList:
            if DSpeed in data:
                speed = speed - 9
                if speed <= 1:
                    speed = 1
        for SpeakR in SpeakRateUpList:
            if SpeakR in data:
                self.SpeakRate = self.SpeakRate + 10
        for SpeakR in SpeakRateDownList:
            if SpeakR in data:
                self.SpeakRate = self.SpeakRate - 10
        for SpeakV in VolumeUpList:
            if SpeakV in data:
                self.SpeakVolume = self.SpeakVolume - 10
        for SpeakV in VolumeDownList:
            if SpeakV in data:
                self.SpeakVolume = self.SpeakVolume - 10
        return speed, dir, servo
