#The part which interacts with audio data

import soundguard_fileop as fileop
import xml.etree.ElementTree as ET
import soundguard_data as sdata
import subprocess

import winsound

# We are getting the audio devices details using SoundVolumeView.exe made by Nirsoft

muteCommand = "..\\Bin\\SoundVolumeView.exe /Mute {}"
switchCommand = "..\\Bin\\SoundVolumeView.exe /SetDefault {}"

setVolumeCommand = "..\\Bin\\SoundVolumeView.exe /SetVolume {} {}"

xmlDataCommand = "..\\Bin\\SoundVolumeView.exe /sxml ..\\Data\\audioinfo.xml"
xmlFileLocation = "..\\Data\\audioinfo.xml"

root = None

def getXmlData(): #Makes a snapshot of all current audio devices info and saves it to audioinfo.xml
    global root
    subprocess.call(xmlDataCommand, shell=True)
    tree = ET.parse(xmlFileLocation)
    root = tree.getroot()

def getDefaultDeviceName():
    if root == None:
        return
    name1 = ""
    name2 = ""
    for child in root:
        for element in child:
            if(element.tag == "name"):
                name1 = element.text
            if(element.tag == "device_name"):
                name2 = element.text
            elif(element.tag == "default"):
                if(element.text == "Render"):
                    return "{} ({})".format(name1, name2)
            else:
                continue
    return None
        
def getDeviceList(): # Returns a list of all enabled output audio devices
    if root == None:
        return
    devices = []
    for child in root:
        is_output = False
        for element in child:
            if(element.tag == "name"):
                name = element.text
            elif(element.tag == "device_name"):
                device_name = element.text
            elif(element.tag == "direction" and element.text == "Render"):
               is_output = True
            elif(element.tag == "device_state"):
                if(element.text != None and element.text != "Unplugged" and element.text != "Disabled" and is_output):
                    devices.append("{} ({})".format(name, device_name))
                    break
            else:
                continue
    return devices

def getDeviceAttribByName(devicename, attrib): #Returns an value of a device from audioinfo.xmf file
    if root == None:
        return
    devicename = devicename.split("(")
    name1 = devicename[0][:len(devicename[0])-1]
    name2 = devicename[1][:len(devicename[1])-1]
    renderRole = False
    item_attrib = None
    for child in root:
        name1found = False
        name2found = False
        for element in child:
            if(element.tag == "name" and element.text == name1):
               name1found = True
            elif(element.tag == "device_name" and element.text == name2):
                name2found = True
            elif(element.tag == "direction" and element.text == "Render"):
                renderRole = True
            elif(element.tag == attrib):
               item_attrib = element.text
            else:
                continue
        if name1found and name2found and renderRole :
            return item_attrib
    return None

    
def muteHeadphones():
    sdata.initData()
    getXmlData()
    device = getDefaultDeviceName()
    subprocess.call(muteCommand.format(getDeviceAttribByName(device, "item_id")), shell=True)

def switchToSpeakers(): #If switch to speakers option is checked, this function will switch to your preffered speaker device IF you are using headphones
    sdata.initData()
    getXmlData()
    speakers = fileop.loadListFromFile(sdata.speakersFile)
    headphones = fileop.loadListFromFile(sdata.headphonesFile)
    currentDevice = getDefaultDeviceName()
    if currentDevice in headphones:
        subprocess.call(switchCommand.format(getDeviceAttribByName(speakers[0], "item_id")), shell=True)

def isMute():
    headphones = fileop.loadListFromFile(sdata.headphonesFile)
    getXmlData()
    device = getDefaultDeviceName()
    if device in headphones:
        if getDeviceAttribByName(device, "muted") == "Yes":
            return True
    return False

def setVolume(device, volume):
    print(setVolumeCommand.format(device, volume))
    subprocess.call(setVolumeCommand.format(device, volume), shell=True)
 
def playSound(): # Plays the sound notification if its checkbox is checked
     winsound.PlaySound('..//Sounds//notification.wav',  winsound.SND_ASYNC | winsound.SND_FILENAME)
    
