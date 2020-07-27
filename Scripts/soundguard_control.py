#This module is used for communication between the service and the controller

import socket

""" Control options:

 l - Reload settigs
 v - Reload volume limit
 p - Pause timer
 c - Resume timer
 r - Reset timer
 d - Disconnect
 t - Request timer status
 m - Request device status
 i - Request pause status

"""

class SoundGuradControlServer: # It runs on the service and waits for commands and requests from the controller

    serversocket = None
    client = None
    running = False
    timer = None
    
    def __init__(self, timer): #In the constructor, we create the server socket
        self.timer = timer
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(("127.0.0.1",  3008))
        

    def serve(self):
        print("Control server started\n")
        self.running = True
        self.serversocket.listen(1)
        while self.running:
            self.client, addr = self.serversocket.accept()
            if addr[0] != "127.0.0.1":
                self.client.close()
                continue
            self.handleClient()
    
    def shutdown(self):
        self.running = False
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(("127.0.0.1", 3008))
        sk.send(b'd')
        sk.close()

    def handleClient(self):
        while True:
            try:
                data = self.client.recv(1)
            except:
                return
            data = data.decode("utf-8")
            if data == "v":
                self.timer.loadVolumeLimit()
            elif data == "l":
                self.timer.loadSettings()
            elif data == "p":
                self.timer.paused = True
            elif data == "c":
                self.timer.paused = False
            elif data == "r":
                self.timer.resetTimer()
            elif data == "d":
                self.client.close()
                return
            elif data == "t":
                self.client.send(str.encode(str(self.timer.toWait[self.timer.currentMode])))
            elif data == "m":
                self.client.send(str.encode(str(self.timer.currentMode)))
            elif data == "i":
                toSend = "0"  
                if self.timer.paused:
                    toSend = "1"
                self.client.send(str.encode(str(toSend)))

class SoundGuardControlClient: # It is used by the controller and, of course, it sends requests and commands to the service
    
    @staticmethod
    def getConnectedSocket():
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sk.connect(("127.0.0.1", 3008))
            return sk
        except:
            return None
        
    @staticmethod
    def sendCommand(command):
        sk = SoundGuardControlClient.getConnectedSocket()
        if sk == None:
            return
        sk.send(str.encode(command))
        sk.send(b'd')
        sk.close()
    
    @staticmethod
    def getTimer():
        sk = SoundGuardControlClient.getConnectedSocket()
        if sk == None:
            return
        sk.send(b't')
        timer = sk.recv(256)
        timer = int(timer.decode("utf-8"))
        sk.send(b'd')
        sk.close()
        return timer
    
    @staticmethod
    def getStatus(stat):
        sk = SoundGuardControlClient.getConnectedSocket()
        if sk == None:
            return None
        sk.send(str.encode(stat))
        mode = sk.recv(1)
        mode = int(mode.decode("utf-8"))
        sk.send(b'd')
        sk.close()
        return mode

    

        
