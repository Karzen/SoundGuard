#The part which makes the GUI usable
from soundguard_control import SoundGuardControlClient as control
import soundguard_gui_monitor as monitor

import soundguard_fileop as fileop
import soundguard_gui as gui
import audio_utils as au

import soundguard_data as sdata

import os

def getSelectedElement(qlist):
    item = qlist.currentItem()
    if item == None:
        return None
    return item.text()

def loadDevices(): #Loads and filters all of the audio devices saved, removes the ones that dont work anymore and adds the new ones
    au.getXmlData()
    sdata.allDevices = au.getDeviceList()
    if os.path.getsize(sdata.headphonesSaveFile) == 0:
        sdata.speakers = sdata.allDevices[:]
        fileop.writeListToFile(sdata.speakersFile, sdata.speakers)
    else:
        sdata.headphones = fileop.loadListFromFile(sdata.headphonesSaveFile)
        sdata.speakers = []
        if os.path.getsize(sdata.speakersFile) != 0:
            sdata.speakers = fileop.loadListFromFile(sdata.speakersFile)
            
        for device in sdata.headphones:
            if device not in sdata.allDevices:
                sdata.headphones.remove(device)
        for device in sdata.allDevices:
            if device not in sdata.headphones and device not in sdata.speakers:
                sdata.speakers.append(device)
                
    updateDevices()
    fileop.writeListToFile(sdata.speakersFile, sdata.speakers)
    fileop.writeListToFile(sdata.headphonesFile, sdata.headphones)


def updateDevices():#Adding devices on the gui
    
    gui.GUI.listWidgetSpeakers.clear()
    gui.GUI.listWidgetHeadphones.clear()
    for device in sdata.speakers:
            gui.GUI.listWidgetSpeakers.addItem(device)
    for device in sdata.headphones:
            gui.GUI.listWidgetHeadphones.addItem(device)

def updateModes():#Adding functioning modes on the gui
    gui.GUI.comboBox.clear()
    for mode in sdata.loadedModes:
        string = "{}:{}:{} Headphones - {}:{}:{} Break".format(
        mode[0][0],mode[0][1],mode[0][2],
        mode[1][0],mode[1][1],mode[1][2])
        gui.GUI.comboBox.addItem(string)
    fileop.writeModesToFile(sdata.modesFile, sdata.loadedModes)

def raiseSelectedElement():
    element = getSelectedElement(gui.GUI.listWidgetSpeakers)
    if element == None:
        return
    index = sdata.speakers.index(element)
    if index > 0:
        
        save = sdata.speakers[index-1]
        sdata.speakers[index-1] = sdata.speakers[index]
        sdata.speakers[index] = save
        updateDevices()
        gui.GUI.listWidgetSpeakers.setCurrentRow(index-1)
        fileop.writeListToFile(sdata.speakersFile, sdata.speakers)
    
def lowerSelectedElement():
    element = getSelectedElement(gui.GUI.listWidgetSpeakers)
    if element == None:
        return
    index = sdata.speakers.index(element)
    if index < len(sdata.speakers)-1:
        save = sdata.speakers[index+1]
        sdata.speakers[index+1] = sdata.speakers[index]
        sdata.speakers[index] = save
        updateDevices()
        gui.GUI.listWidgetSpeakers.setCurrentRow(index+1)
        fileop.writeListToFile(sdata.speakersFile, sdata.speakers)

def swapToHeadphones(): #Swaps the selected device from speakers section to headphone section
    element = getSelectedElement(gui.GUI.listWidgetSpeakers)
    if element == None:
        return
    sdata.speakers.remove(element)
    sdata.headphones.append(element)
    updateDevices()
    fileop.addElementToFile(sdata.headphonesSaveFile, element)
    fileop.writeListToFile(sdata.speakersFile, sdata.speakers)
    fileop.writeListToFile(sdata.headphonesFile, sdata.headphones)
    
def swapToSpeakers(): #The inverse of the one above
    element = getSelectedElement(gui.GUI.listWidgetHeadphones)
    if element == None:
        return
    sdata.headphones.remove(element)
    sdata.speakers.append(element)
    updateDevices()
    fileop.removeElementFromFile(sdata.headphonesSaveFile, element)
    fileop.writeListToFile(sdata.speakersFile, sdata.speakers)
    fileop.writeListToFile(sdata.headphonesFile, sdata.headphones)

def updateSliderValue():#Links the slider to the spinbox
    sdata.volumeLimit = gui.GUI.horizontalSlider.value()
    gui.GUI.spinBox_7.setValue(sdata.volumeLimit)
    fileop.writeListToFile(sdata.volumeLimitFile, [sdata.volumeLimit])
    monitor.toSend.append("v")
    
def updateSpinBoxValue():#The inverse of the one above again
    sdata.volumeLimit = gui.GUI.spinBox_7.value()
    gui.GUI.horizontalSlider.setValue(sdata.volumeLimit)
    fileop.writeListToFile(sdata.volumeLimitFile, [sdata.volumeLimit])
    monitor.toSend.append("v")
    
def loadModes(): #Loads the saved functioning modes
    if os.path.getsize(sdata.modesFile) > 0:
        sdata.loadedModes = fileop.loadModesFromFile(sdata.modesFile)
    else:
        restoreDefaultModes()
    if os.path.getsize(sdata.currentModeFile) > 0:
        sdata.currentMode = int(fileop.loadListFromFile(sdata.currentModeFile)[0])
        if sdata.currentMode == -1:
            sdata.currentMode = 0
    else:
        fileop.writeListToFile(sdata.currentModeFile, [sdata.currentMode])
    
    updateModes()
    gui.GUI.comboBox.setCurrentIndex(sdata.currentMode)

def updateCurrentMode(mode):
    sdata.currentMode = mode
    fileop.writeListToFile(sdata.currentModeFile, [mode])
    monitor.toSend.append("l")

def removeMode():
    index = gui.GUI.comboBox.currentIndex()
    if index != -1:
        del sdata.loadedModes[index]
        updateModes()
        if index > 0:
            gui.GUI.comboBox.setCurrentIndex(index-1)

def restoreDefaultModes():
    sdata.loadedModes = sdata.defaultModes[:]
    updateModes()
    

def checkSpinBoxes(): #Verifies if the spinboxes where you add the volume are not empty
    return (gui.GUI.spinBox.value() != 0 or \
            gui.GUI.spinBox_2.value() != 0 or\
            gui.GUI.spinBox_3.value() != 0) and \
            (gui.GUI.spinBox_4.value() != 0 or
            gui.GUI.spinBox_5.value() != 0 or
            gui.GUI.spinBox_6.value() != 0)
            
def getModeFromSpinBoxes():
    return [ [gui.GUI.spinBox.value(),gui.GUI.spinBox_2.value(),gui.GUI.spinBox_3.value()],
             [gui.GUI.spinBox_4.value(),gui.GUI.spinBox_6.value(),gui.GUI.spinBox_5.value()]
           ]

def addMode():
    if not checkSpinBoxes():
        gui.showErrorPopup("Error", sdata.errorModeAddText)
    else:
        mode = getModeFromSpinBoxes()
        if mode not in sdata.loadedModes:
            sdata.loadedModes.append(mode)
            updateModes()
            gui.GUI.comboBox.setCurrentIndex(gui.GUI.comboBox.count()-1)
        else:
            gui.showErrorPopup("Error", sdata.errorModeAlreadyAddedText)

def loadSettings(): #Loads the settings
    print(sdata.settingsCheckBoxesStates)
    if os.path.getsize(sdata.settingsCheckBoxFile) != 0:
        sdata.settingsCheckBoxesStates = fileop.loadBoolArrayFromFile(sdata.settingsCheckBoxFile)
    else:
        fileop.saveBoolArrayToFile(sdata.settingsCheckBoxFile, sdata.settingsCheckBoxesStates)
    
    for setting in sdata.settingsCheckBoxesList:
        if sdata.settingsCheckBoxesStates[sdata.settingsCheckBoxesList.index(setting)]:
            setting.setCheckState(2)
        else:
            setting.setCheckState(0)
            pass

    if os.path.getsize(sdata.volumeLimitFile) != 0:
        sdata.volumeLimit = fileop.loadListFromFile(sdata.volumeLimitFile)[0]
        gui.GUI.horizontalSlider.setValue(int(sdata.volumeLimit))
        
        
