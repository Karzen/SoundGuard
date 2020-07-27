#The part of the controller that sends commands to the service

from soundguard_control import SoundGuardControlClient as control
import soundguard_gui as gui
from PyQt5 import QtCore, QtGui, QtWidgets

import time

headphoneImg = "..\\Icons\\headphones.png"
speakerImg = "..\\Icons\\speaker.png"

pause = False
stop = False
toSend = []

def updateTimer(): #Decides if the controller will show the speaker time or the headphone time
    global pause, stop
    while True:
        mode = None
        sec = None
        while sec == None or mode == None and not pause:
            sec = control.getTimer()
            mode = control.getStatus("m")
            
        if mode == 0:
            gui.GUI.label_2.setPixmap(QtGui.QPixmap(headphoneImg))
            gui.GUI.label_13.setText("Headphone time")
        else:
            gui.GUI.label_2.setPixmap(QtGui.QPixmap(speakerImg))
            gui.GUI.label_13.setText("Speaker time")
        gui.GUI.label_13.adjustSize()
        stop = True
        doTimer(sec)

def doTimer(seconds): #We request the seconds from the service until it reaches 0
    global pause,stop
    while seconds > 0:
        if not pause:
            seconds = control.getTimer()
            gui.GUI.label.setText(buildString(seconds))
            gui.GUI.label.adjustSize()
            time.sleep(0.5)
            if stop:
                return

def buildString(seconds): #Converting seconds to hours:minutes:seconds format
        hours = 0
        minutes = 0
        if seconds >= 3600:
            hours = int(seconds/3600)
            seconds -= hours*3600
        if seconds >= 60:
            minutes = int(seconds/60)
            seconds -= minutes*60
        
        return f"{hours}:{minutes}:{seconds}"


def transmissionManager():#For optimization purposes, this is the part which actually sends the commands to the service once a second
    global toSend, pause
    while True:
        send = list(set(toSend)) #Again, for optimization and stability purposes, we send only one of each command type
        toSend = []
        for command in send:
            control.sendCommand(command)
        if control.getStatus("i") == 1:
            pause = True
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("../Icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            gui.GUI.pushButton_10.setIcon(icon1)
        else:
            pause = False
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("../Icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            gui.GUI.pushButton_10.setIcon(icon1)
            
        time.sleep(1)
            
            
