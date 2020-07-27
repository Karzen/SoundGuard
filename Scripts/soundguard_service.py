#This is the service which runs in the background, and monitors your audio stuff
from soundguard_control import SoundGuradControlServer

import soundguard_fileop as fileop
import soundguard_data as sdata
import audio_utils as au
import popup

import threading
import time
import os

import win32gui
import win32con

class Timer:

    runMode = [30*60, 10*60]
    toWait = [0, 0]
    paused = False
    timerRunning = False
    abort = False
    isBreak = False

    currentMode = 0

    wasReset = False
    wasMute = False
    
    endPopup = False
    endMute = False
    endSwitch = False
    endSound = False
    limitVolume = False
    limitVolumeValue = 100
    stopWhenMute = False
    
    autoreset = False

    
    def __init__(self):
        sdata.initData()
        self.loadSettings()
            
        
    def loadSettings(self):
        fileop.checkDataFilesExist()
        if os.path.getsize(sdata.settingsCheckBoxFile) > 0:
            boolList = fileop.loadBoolArrayFromFile(sdata.settingsCheckBoxFile)
            self.endPopup = boolList[3]
            self.endSwitch = boolList[0]
            self.endMute = boolList[1]
            self.endSound = boolList[2]
            self.limitVolume = boolList[5]
            self.stopWhenMute = boolList[6]
        self.loadVolumeLimit()
        if os.path.getsize(sdata.modesFile) > 0 and os.path.getsize(sdata.currentModeFile):
            modeIndex = int(fileop.loadListFromFile(sdata.currentModeFile)[0])
            self.runMode = self.getWaitTimeInSeconds(fileop.loadModesFromFile(sdata.modesFile)[modeIndex])

    def loadVolumeLimit(self):
        if os.path.getsize(sdata.volumeLimitFile) > 0:
            self.limitVolumeValue = int(fileop.loadListFromFile(sdata.volumeLimitFile)[0])
    
    def buildString(self, seconds):#Converting seconds to hours:minutes:seconds format
        hours = 0
        minutes = 0
        if seconds >= 3600:
            hours = int(seconds/3600)
            seconds -= hours*3600
        if seconds >= 60:
            minutes = int(seconds/60)
            seconds -= minutes*60
        
        return f"{hours}:{minutes}:{seconds}"
    
    def getWaitTimeInSeconds(self, mode): #Converts the hours:minutes:seconds format into seconds only
        return [mode[0][0]*3600+mode[0][1]*60+mode[0][2],
                mode[1][0]*3600+mode[1][1]*60+mode[1][2]]
        
    def startTimer(self, mode = 0): #The actual timer if mode = 0 then its headphone time, else if mode = 1 then is break time
        print("starting a new timer")
        print(self.toWait)
        self.timerRunning = True
        self.currentMode = mode
        while self.toWait[mode] != 0:
            if not self.paused:
                print("running " + str(mode))
                time.sleep(1)
                self.toWait[mode] -= 1
                self.tickUpdate()
            elif self.abort:
                break
        self.timerRunning = False
        if not self.abort:
            self.timerEnd(mode)
        

    def stopTimer(self):
        self.paused = True
        self.abort = True
        while self.timerRunning:
            continue
        self.abort = False
        self.paused = False

    def resetTimer(self):
        self.wasReset = True
        self.stopTimer()
        self.toWait = self.runMode[:]
        
    def tickUpdate(self): #This method is called every second and runs the other methods monitoring your device
        if self.endPopup and self.isBreak and popup.isActive:
            self.updatePopup()
        if self.limitVolume and self.currentMode == 0 and self.timerRunning :
            self.checkVolume()
        if self.stopWhenMute and au.isMute():
            threading.Thread(target=monitorMuteState, args=(self,)).start()
        

    def checkVolume(self): #If the limit volume setting is enabled and the sound limit is exceeded, then, it sets your volume to the limit
        au.getXmlData()
        device = au.getDefaultDeviceName()
        volume = au.getDeviceAttribByName(device, "volume_percent")
        volume = int(float(volume[:-1]))
        device = au.getDeviceAttribByName(device, "item_id")
        if volume > self.limitVolumeValue:
            au.setVolume(device, self.limitVolumeValue)
        
    def isHeadphone(self, device):
        headphones = fileop.loadListFromFile(sdata.headphonesFile)
        return device in headphones
    
    def timerEnd(self, mode): #This method runs when the timer has ended
        print(mode)
        if mode == 0:
            self.isBreak = True
            if self.endPopup and not self.isControllerActive():
                threading.Thread(target=self.popupEvent).start()
            if self.endSound:
                self.playSoundEvent()
            if self.endSwitch:
                self.switchEvent()
            if self.endMute:
                self.muteEvent()
            
        if mode == 1:
            if popup.isActive:
                popup.hidePopup()  
    
    def popupEvent(self): #Is showing the popup
        popup.createPopup() 
        popup.POP.pushButton.clicked.connect(popup.hidePopup)
        popup.POP.label.setText(self.buildString(self.toWait[1]))
        threading.Thread(target=self.raisePopup).start()
        popup.showPopup()
            
    def updatePopup(self): #Update the timer on the popup
        try:
            popup.POP.label.setText(self.buildString(self.toWait[1]))
        except:
            self.popupExists = False

    def raisePopup(self): # It raises the popup above all the windows on the screen
        while not popup.isActive:
            continue
        try:
            hWnd = win32gui.FindWindow(None, popup.popupTitle)
            if hWnd != None:
                win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0,0,0,0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except:
            pass

    def isControllerActive(self): #Returns true if the controller is active and false otherwise
        try:
            hWnd = win32gui.FindWindow(None, "SoundGuard")
            print(hWnd)
            if hWnd == None or hWnd == 0:
                return False
            return True
        except:
            return False

    def playSoundEvent(self): #Plays the soudn notification
        au.playSound()
        
    def switchEvent(self): # Switches to your preffered speaker when the time comes up
        au.switchToSpeakers()
        
    def muteEvent(self): #Mutes the volume       
        au.muteHeadphones()
    


def monitorMuteState(t): #It stops the timer if the headphones are muted
    t.paused = True
    while True:
        if not au.isMute() or not t.stopWhenMute:
            t.paused = False
            break
        time.sleep(1)
            


if __name__ == "__main__": # And we are finally running the service

    t = Timer()
    server = SoundGuradControlServer(t)
    threading.Thread(target = server.serve).start() #Running the server waiting for the commands on another thread
    
    while True:
        t.toWait = t.runMode[:] # It does the headphone-speaker cycle
        t.startTimer()
        if t.wasReset:
            t.wasReset = False
            continue
        t.startTimer(1)
        


