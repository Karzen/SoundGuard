#The app is made of 2 parts : The service and the controller

#This file will start both of them

#The service is the actual script thet runs in the background and monitors your audi activity

#The controller is the GUI part which changes the settings and communicate with the service

from soundguard_control import SoundGuardControlClient as control

import soundguard_gui_monitor as monitor #The part which communicates with the service
import soundguard_gui_utils as gutil     #The part which makes the GUI usable
import soundguard_fileop as fileop       #The part used for file interaction (saving settings)
import soundguard_data as sdata          #The part which stores all of the strings and details of the app
import soundguard_gui as gui             #The actual GUI made using PyQt5
import audio_utils as au                 #The part which interacts with audio data

from psutil import process_iter
from subprocess import call
import threading
import os

def connectButtons(): #Links the buttons to their corresponding function
    gui.GUI.InfoButton3.clicked.connect(lambda : gui.showInfoPopup(sdata.audioDevicesInfoTitle, sdata.audioDevicesInfoText))
    gui.GUI.pushButton.clicked.connect(gutil.raiseSelectedElement)
    gui.GUI.pushButton_2.clicked.connect(gutil.lowerSelectedElement)
    gui.GUI.pushButton_3.clicked.connect(gutil.swapToSpeakers)
    gui.GUI.pushButton_4.clicked.connect(gutil.swapToHeadphones)
    gui.GUI.pushButton_6.clicked.connect(gutil.addMode)
    gui.GUI.pushButton_7.clicked.connect(gutil.restoreDefaultModes)
    gui.GUI.pushButton_8.clicked.connect(gutil.removeMode)
    gui.GUI.refreshButton.clicked.connect(gutil.loadDevices)
    gui.GUI.pushButton_10.clicked.connect(pauseStatusChange)
    gui.GUI.pushButton_9.clicked.connect(resetTimer)

def connectCheckBoxes(): #Same as for check boxes
    sdata.initCheckBoxes()
    gui.GUI.checkBox_2.stateChanged.connect(lambda state: editSettings(state, 0)) #SwitchToSpeakers
    gui.GUI.checkBox_3.stateChanged.connect(lambda state: editSettings(state, 1)) #Mute
    gui.GUI.checkBox_4.stateChanged.connect(lambda state: editSettings(state, 2)) #PlaySound
    gui.GUI.checkBox_5.stateChanged.connect(lambda state: editSettings(state, 3)) #Popup
    gui.GUI.checkBox_6.stateChanged.connect(lambda state: startupCopy(state))     #Startup
    gui.GUI.checkBox_7.stateChanged.connect(lambda state: editSettings(state, 5)) #LimitVolume
    gui.GUI.checkBox_8.stateChanged.connect(lambda state: editSettings(state, 6)) #HeadphoneMuteStop
    
    
    gutil.loadSettings()

def connectMisc(): #This links some miscellaneous parts
    gui.GUI.horizontalSlider.valueChanged.connect(gutil.updateSliderValue)
    gui.GUI.spinBox_7.valueChanged.connect(gutil.updateSpinBoxValue)
    gui.GUI.comboBox.currentIndexChanged.connect(lambda index: gutil.updateCurrentMode(index))


def pauseStatusChange(): #The pause button function
    if monitor.pause:
        monitor.toSend.append("c")
    else:
        monitor.toSend.append("p")

def resetTimer():
    monitor.toSend.append("r")
    monitor.stop = True
    

def editSettings(state, index):
    if state == 2:
        state = True
    else:
        state = False
    
    sdata.settingsCheckBoxesStates[index] = state
    fileop.saveBoolArrayToFile(sdata.settingsCheckBoxFile, sdata.settingsCheckBoxesStates)
    monitor.toSend.append("l")


def startupCopy(state): # If state = True: create a batch file in the startup folder which runs the service when windows is starting
    editSettings(state, 4) # If state = False it deletes the batch file
    startupFile = os.getenv("AppData") + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\SoundGuard.bat"
    if state == 2:
        if os.path.exists(sdata.serviceFile) and os.path.getsize(sdata.serviceFile) > 0:
            f = open(sdata.serviceFile, 'r')
            name = f.read()
            f.close()
            try:
                f = open(startupFile, "w")
                f.write('start "" {} \nexit'.format(os.path.abspath(name)))
                f.close()
            except:
                return
    else:
        os.remove(startupFile)

def checkTimerRunning(): #Checks if the service is running and runs it, if its not
    try:
        f = open(sdata.serviceFile, 'r')
        name = f.read()
        f.close()
    except:
        gui.showErrorPopup("Error at running the service", "The soundguard_service could not start, you can manually fix this by running the soundguard_service.exe file ")
    
    for process in process_iter():
        if process.name() == name:
            return
    try:
        print("run")
        call('start "" {}'.format(name), shell=True)
    except:
        gui.showErrorPopup("Error at running the service", "The soundguard_service could not start, you can manually fix this by running the soundguard_service.exe file ")
    
        
    
 
if __name__ == "__main__":  #And finally we are running the script
    sdata.initData()
    fileop.checkDataFilesExist()
    gui.createUI()
    connectButtons()
    gutil.loadModes()
    gutil.loadDevices()
    connectMisc()
    connectCheckBoxes()
    checkTimerRunning()
    threading.Thread(target=monitor.transmissionManager).start()
    threading.Thread(target=monitor.updateTimer).start()
    gui.showUI()
    
    
