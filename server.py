################################################
# Imports
################################################
# Used to setup server handler
import os

try:
    import socketserver

    OPERATE = True

except:
    print("Need Python3 to operate server")
    OPERATE = False

# To "exe" and binary file paths
import shutil

# Used to get OS Type
import platform

# Used to get serverIP
import socket

# Used to setup logging
import logging
import logging.config

# Used to display logging to stdout
import sys

# Used for Current Time
from datetime import datetime

# For threading processes
import threading

###############################################
# Global Variables
###############################################
# Get operating system
OS = platform.system()
defaultPath = os.getcwd()

# Mutexes and Semaphores
modifyMutex = threading.Lock()
numberOfMaxReaders = 20
readSemaphore = threading.Semaphore(numberOfMaxReaders)


###############################################
# Classes
###############################################

###############################################
# fileServer child Class
# Super class is socketServer.TCPServer
class fileServer(socketserver.TCPServer):

    # __init__ ("fileServer" child class)
    def __init__(self, IP, childHandler):
        #######################################
        # Create Unique Server Variables
        #######################################

        # Valid Users and Password
        self.authorizedUsers = ["admin", "password", "bob", "1234", "alice", "abcd"]

        # Users Online
        self.activeUsers = []

        # Save Port Number, IP
        self.serverPort = 50000
        self.serverIP = IP

        #######################################
        # Set Logging Objects
        #######################################

        # Set logging configuration
        logging.basicConfig(filename='fileServer.log', level=logging.DEBUG, filemode='w',
                            format='%(asctime)s\t\tLogger: %(name)s\t\tLevel: %(levelname)s\t\tEvent: %(message)s',
                            datefmt='%Y:%m:%d %H:%M:%S')

        # Create Logger
        self.serverLog = logging.getLogger("Server")

        # Create Handler, set level to at least DEBUG
        loggingHandler = logging.StreamHandler(sys.stdout)
        self.serverLog.addHandler(loggingHandler)

        # Post to log, "File Server Started"
        date = datetime.now().strftime("DATE: %Y:%m:%d\tTIME: %H:%M:%S\t\tEVENT: ")
        print("%s" % date, end="")
        self.serverLog.info("File Server Started\tNote: @IP: % s" % self.serverIP)

        # Call Super Class "TCPServer", to __init__ Child TCPServer Class
        socketserver.TCPServer.__init__(self, (self.serverIP, self.serverPort), childHandler)
        return


##############################################
# fileServerHandler child class
# Super class is socketserver.BaseRequestHandler
# Class instance to handle server requests
class fileServerHandler(socketserver.BaseRequestHandler):

    # __init__ ("fileServerHandler" child class)
    def __init__(self, requestType, clientIP, serverIP):
        #######################################
        # Set Logging Objects
        #######################################

        # Set logging configuration
        logging.basicConfig(filename='fileServer.log', level=logging.DEBUG, filemode='w',
                            format='%(asctime)s\t\tLogger: %(name)s\t\tLevel: %(levelname)s\t\tEvent: %(message)s',
                            datefmt='%Y:%m:%d %H:%M:%S')

        # Create serverHandler Logger
        self.serverHandlerLog = logging.getLogger("Server Handler")

        # Create Handler
        loggingHandler = logging.StreamHandler(sys.stdout)
        self.serverHandlerLog.addHandler(loggingHandler)

        # Post to log, "File Server Started"
        print(datetime.now().strftime("DATE: %Y:%m:%d\tTIME: %H:%M:%S\t\tEVENT: "), end="")
        self.serverHandlerLog.info("File Handler Started")

        # Call Super Class "BaseRequestHandler", to __init__ Child Handler Class
        socketserver.BaseRequestHandler.__init__(self, requestType, clientIP, serverIP)
        return

    # NEEDED!!!
    # handle() method must be implemented to override the super class
    def handle(self):
        # print("Server handler looking for NEW connection")

        # Receive Data
        data = self.request.recv(1024).decode()

        # Log About received data
        self.serverHandlerLog.info("[+] New Connection Made, IP: %s, Port: %s" % self.client_address)

        # Split data into an array
        dataArray = data.split()
        print("TEST: Client sent %s" % dataArray)

        # Send back ACK
        self.request.sendall("ACK".encode())
        return


##############################################
# fileObject
# Contains USEFUL info about a file
# Including a mutex for writing and syncing
class fileObject:

    def __int__(self, name, type, owner):
        self.TYPE = type
        self.OWNER = owner
        self.ACCESS_LIST = []
        self.NAME = name

        # Dont know how to implement
        self.PATH = None

        # If object is a directory we can use this
        self.subDirectories = []
        self.subFiles = []

    # Sets file/directory path
    def setPath(self, path):
        self.PATH = path

    # Appends a subDirectory
    def makeNewDirectory(self, path, name, user):

        print("Not Tested")

        # Get to Directory to ADD NEW
        if (len(path) == 0):

            # Error for NAME already exists
            for i in self.subDirectories:

                if i.NAME == name:
                    print("Error, NAME already exists")
                    return False

            # Make new fileObject in subDirectory
            newDirectory = fileObject()
            newDirectory.TYPE = "D"
            newDirectory.NAME = name
            newDirectory.OWNER = user
            self.subDirectories.append(fileObject)
            print("Test Code, directory made")
            return True

        # Else "recursive call" to FIND
        for i in self.subDirectories:

            if i.NAME == path[0]:
                return i.makeNewDirectory(self, path[1:], name, user)

        path.join("/")
        print("Error, rest of PATH: '%s' not found" % path)
        return False


    def makeNewFile(self, path, name, user):

        print("Not Tested")

        # Get to Directory to ADD NEW
        if (len(path) == 0):

            # Error for NAME already exists
            for i in self.subFiles:

                if i.NAME == name:
                    print("Error, NAME already exists")
                    return False

            # Make new fileObject in subFiles
            newFile = fileObject()
            newFile.TYPE = "F"
            newFile.NAME = name
            newFile.OWNER = user
            self.subFiles.append(fileObject)
            print("Test code, file made")

            return True

        # Else "recursive call" to FIND
        for i in self.subDirectories:

            if i.NAME == path[0]:
                return i.makeNewFile(self, path[1:], name, user)

        path.join("/")
        print("Error, rest of PATH: '%s' not found" % path)
        return False

    # Return True or False if name matches
    def checkName(self, name):
        if self.NAME == name:
            return True
        else:
            return False


    # Passed a name, return a list of file permissions
    # Check permissions of a valid file
    def returnUserIndex(self, user):

        print("Not Implemented/Checked")

        # Search all ACCESS_LIST for user name
        for i in range(len(self.ACCESS_LIST)):

            # if user found, return index location
            if self.ACCESS_LIST[i] == user:
                return int(i)

            else:
                i += 4

        # Else return there is no user found
        return -1

    # Add sub permission to file type
    def addPermission(self, user, read, write, delete, rename):
        self.ACCESS_LIST.append(user)
        self.ACCESS_LIST.append(read)
        self.ACCESS_LIST.append(write)
        self.ACCESS_LIST.append(delete)
        self.ACCESS_LIST.append(rename)

    # Changes permissions of sub-users
    def changePermission(self, user, read, write, delete, rename):

        print("Not Implemented/Checked")

        # Look for index of User
        index = self.returnUserIndex(self, user)

        if self.OWNER == user:
            print("OWNER has super permission, cannot change")
            return

        elif index == -1:
            print("User not found to change permissions")
            return

        else:
            self.ACCESS_LIST[index + 1] = read
            self.ACCESS_LIST[index + 2] = write
            self.ACCESS_LIST[index + 3] = delete
            self.ACCESS_LIST[index + 4] = rename

    # Checks read access
    def checkRead(self, name):

        print("Not Implemented/Checked")

        if name == self.OWNER:
            return True

        for i in range(len(self.ACCESS_LIST)):

            # Both Name and Read == TRUE
            if self.ACCESS_LIST[i] == name:
                if self.ACCESS_LIST[i + 1]:
                    return True
                else:
                    return False

            # CYCLE through
            else:
                i += 4

        # Default return False
        return False

    # Checks write access
    def checkWrite(self, name):

        print("Not Implemented/Checked")

        if name == self.OWNER:
            return True

        for i in range(len(self.ACCESS_LIST)):

            # Both Name and Write == TRUE
            if self.ACCESS_LIST[i] == name:
                if self.ACCESS_LIST[i + 2]:
                    return True
                else:
                    return False

            # CYCLE through
            else:
                i += 4

        # Default return False
        return False

    # Checks delete access
    def checkDelete(self, name):

        print("Not Implemented/Checked")

        if name == self.OWNER:
            return True

        for i in range(len(self.ACCESS_LIST)):

            # Both Name and Write == TRUE
            if self.ACCESS_LIST[i] == name:
                if self.ACCESS_LIST[i + 3]:
                    return True
                else:
                    return False

            # CYCLE through
            else:
                i += 4

        # Default return False
        return False

    # Checks rename access
    def checkRename(self, name):

        print("Not Implemented/Checked")

        if name == self.OWNER:
            return True

        for i in range(len(self.ACCESS_LIST)):

            # Both Name and Write == TRUE
            if self.ACCESS_LIST[i] == name:
                if self.ACCESS_LIST[i + 4]:
                    return True
                else:
                    return False

            # CYCLE through
            else:
                i += 4

        # Default return False
        return False



    # Parameter is a LIST
    # CONTAINS THE FULL PATH TO CHECK
    # Checks to see if path exists
    def checkPath(self, list_of_path):

        # Could be file or Directory, if last one
        if len(list_of_path) == 1:

            for i in self.subDirectories:
                if i.NAME == list_of_path[0]:
                    return True

            for i in self.subFiles:
                if i.NAME == list_of_path[0]:
                    return True

            # Default Return False
            return False

        # Continue searching Directories
        for i in self.subDirectories:
            if i.NAME == list_of_path[0]:
                fileObject.checkPath(i, list_of_path[1:])
                break

        # By default, return False
        return False

    # Check to see if name already exists in "path"
    def listFilesAndDirectories(self, list_of_path):

        if len(list_of_path) == 0:
            for i in self.subDirectories:
                print("[D] ", i.NAME)

            for i in self.subFiles:
                print("[F] ", i.NAME)

            return

        for i in self.subDirectories:
            if i.NAME == list_of_path[0]:
                fileObject.checkPath(i, list_of_path[1:])
                break

        print("Directory doesn't exist")
        return


################################
# Non class functions
################################

# Gets notepad on Windows, Nano on Linux
def openTextEditor():
    if OS == "Windows":
        return shutil.which("notepad")

    elif OS == "Linux":
        return shutil.which("nano")


def deleteFile():
    print("not yet implement")


def createBaseDirectory(name, path):
    # Check if PATH exists
    pathExists = BaseDirectory.checkPath(path)
    if not pathExists:
        print("Error, PATH does not exists")
        return

    # Check if NAME already exists
    pathWithName = path.append(name)
    pathExists = BaseDirectory.checkPath(pathWithName)
    if pathExists:
        print("Error, NAME already exists")
        return


# BaseDirectory Object
BaseDirectory = fileObject()
BaseDirectory.NAME = "SEDFS_root"
BaseDirectory.TYPE = "D"
BaseDirectory.OWNER = "root"
BaseDirectory.PATH = defaultPath

# OS PATH w/ BaseServerDirectory NAME
BaseServerPath = os.path.join(defaultPath, BaseDirectory.NAME)


# Try to delete EXISTING DIRECTORY
try:
    os.remove(BaseServerPath)
    os.makedirs(BaseServerPath)

except:
    print("Error: %s : %s" % (BaseServerPath, OSError.strerror))



# Main
if __name__ == '__main__':

    # If Python3 is setup, we can start server
    if OPERATE:
        # Set Server IP
        serverHost = socket.gethostname()
        serverIP = socket.gethostbyname(serverHost)

        # Make fileServer() Object, with (socket) and fileServerHandler
        startFileServer = fileServer(serverIP, fileServerHandler)

        startFileServer.serve_forever()

        # fileServerHandler.request.recv(1024)
        # Makes FileServer run indefinitely
        # startFileServer.serve_forever()
        # startFileServer.get_request()
