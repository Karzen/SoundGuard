#The part which stores all of the strings and details of the app

import soundguard_gui as gui

def initData(): #We need to call this function in order to make these variables "SuperGlobal"
    global speakers,headphones,alldeveices,loadedModes,defaultModes,appSettings,speakersFile,\
           headphonesFile,headphonesSaveFile,modesFile,settingsCheckBoxFile,dataFiles, \
           audioDevicesInfoText, audioDevicesInfoTitle, errorModeAddText, errorModeAlreadyAddedText,\
           settingsCheckBoxesList, settingsCheckBoxesStates, currentMode, currentModeFile, \
           volumeLimitFile, volumeLimitm, serviceFile
           
           
    speakers = []
    headphones = []
    allDevices = []

    loadedModes = []
    defaultModes = [
        [ [0,30,0], [0,5,0] ],
        [ [1,0,0], [0, 10, 0]]
        ]

    currentMode = 0
    volumeLimit = 0

    appSettings = {"SwitchToSpeakers":False,
                   "PlaySound": False,
                   "Popup":False,
                   "Mute":False,
                   "Startup":False,
                   "HeadphoneMuteStop":False,
                   "LimitVolume":False}


    speakersFile = "..//Data//speakers.sdconf"
    headphonesFile = "..//Data//headphones.sdconf"
    headphonesSaveFile = "..//Data//saved_headphones.sdconf"
    modesFile = "..//Data//function_modes.sdmode"
    settingsCheckBoxFile = "..//Data//settings.sdbin"
    currentModeFile = "..//Data//selectedMode.sdconf"
    volumeLimitFile = "..//Data//limiter.sdconf"
    serviceFile = "..//Data//service.sdconf"

    dataFiles = [speakersFile, headphonesFile, headphonesSaveFile, modesFile,
                 settingsCheckBoxFile, currentModeFile, volumeLimitFile]

    audioDevicesInfoText = "Transfer your headphone devices into their section and raise your favorite speaker to the top"
    audioDevicesInfoTitle = "Info"

    errorModeAddText = "Error : 'Headphone' and 'Pause time' fields mut not be empty"
    errorModeAlreadyAddedText = "Error : Functioning mode already exists "

    settingsCheckBoxesList = []
    settingsCheckBoxesStates = [True,False,True,True,True,False,False]





def initCheckBoxes():#When the function above is called, the GUI object is not created, so we will call this function later
    global settingsCheckBoxesList
    settingsCheckBoxesList = [gui.GUI.checkBox_2,gui.GUI.checkBox_3,
                      gui.GUI.checkBox_4,gui.GUI.checkBox_5,
                      gui.GUI.checkBox_6,gui.GUI.checkBox_7,
                      gui.GUI.checkBox_8]
    
