################################################
# Imports
################################################
# Used to setup server handler
import os
from typing import List

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

# Used for Sleeping
import time

###########################################################################
# Global Variables
###########################################################################
# Get operating system
OS = platform.system()

# Get executable path, replace '\' with '/'
defaultSystemPath = os.getcwd().replace("\\", "/") + "/"


# Base Directory
BaseDirectory = "SEDFS_root/"

# NOT IMPLEMENTED
# Mutexes and Semaphores
modifyMutex = threading.Lock()
numberOfMaxReaders = 20
readSemaphore = threading.Semaphore(numberOfMaxReaders)

# Users and Password
authorizedUsers = []

#######################################
# Global Logger
#######################################
# Set logging configuration
logging.basicConfig(filename='fileServer.log', level=logging.DEBUG, filemode='w',
                    format='%(asctime)s\t\tLogger: %(name)s\t\tLevel: %(levelname)s\t\tEvent: %(message)s',
                    datefmt='%Y:%m:%d %H:%M:%S')

# Create Logger
serverLog = logging.getLogger("Server")

# Create Handler, set level to at least DEBUG
loggingHandler = logging.StreamHandler(sys.stdout)
serverLog.addHandler(loggingHandler)


###############################################
# Classes
###############################################

# fileServer child Class
# Super class is socketServer.TCPServer
class fileServer(socketserver.TCPServer):

    # __init__ ("fileServer" child class)
    def __init__(self, IP, childHandler):
        #######################################
        # Create Unique Server Variables
        #######################################

        # Users Online
        self.activeUsers = []

        # Save Port Number, IP
        self.serverPort = 50000
        self.serverIP = IP

        # Post to log, "File Server Started"
        date = datetime.now().strftime("DATE: %Y:%m:%d\tTIME: %H:%M:%S\t\tEVENT: ")
        print("%s" % date, end="")
        serverLog.info("File Server Started\tNote: @IP: % s" % self.serverIP)

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

        # Call Super Class "BaseRequestHandler", to __init__ Child Handler Class
        socketserver.BaseRequestHandler.__init__(self, requestType, clientIP, serverIP)
        return

    # NEEDED!!!
    # handle() method must be implemented to override the super class
    def handle(self):

        # Post to log, "File Server Started"
        print(datetime.now().strftime("DATE: %Y:%m:%d\tTIME: %H:%M:%S\t\tEVENT: "), end="")
        serverLog.info("[+] SEDFS Handle Started")

        # Receive USER info
        user = self.request.recv(1024).decode()

        # Log About received data
        serverLog.info("[+] New Connection Made, IP: %s, Port: %s USER: %s" %
                       (self.client_address[0], self.client_address[1], user))

        # Loop to look for USER
        i = 0
        while i < len(authorizedUsers):

            if authorizedUsers[i] == user:
                self.request.sendall("PASSWORD".encode())
                break

            i += 2

        # if i > len(authorizedUsers) --> Then user does not exist
        if i > len(authorizedUsers):
            self.request.sendall("LOGIN_FAILED".encode())
            serverLog.info("[+] LOGIN FAILED (Invalid USER), IP: %s, Port: %s USER: %s" %
                           (self.client_address[0], self.client_address[1], user))
            return

        # PASSWORD response from client
        password = self.request.recv(1024).decode()

        # Else, "j" is within bounds of authorizedUsers
        if password == authorizedUsers[i + 1]:
            self.request.sendall("LOGIN_SUCCESS".encode())
            serverLog.info("[+] LOGIN SUCCESS, IP: %s, Port: %s USER: %s" %
                           (self.client_address[0], self.client_address[1], user))

        else:
            self.request.sendall("LOGIN_FAILED".encode())
            serverLog.info("[+] LOGIN FAILED (Invalid PASSWORD), IP: %s, Port: %s USER: %s" %
                           (self.client_address[0], self.client_address[1], user))
            return

        # Get userRequest
        request = self.request.recv(1024).decode()
        request = request.split()

        if request[0] == "WRITE":
            print("Server WRITE not implemented / TESTED")
            data = self.receiveALL()
            serverLog.info("[+] '%s' WRITE REQUEST, IP: %s, Port: %s Message: %s" %
                           (user, self.client_address[0], self.client_address[1], data))

            # Try WRITE new directory
            if request[1] == "D":

                try:

                    newDircAt = defaultSystemPath + BaseDirectory + request[3]
                    print("Trying to make a directory at %s" %newDircAt)
                    os.mkdir(newDircAt)
                    print("Server Made new directory")
                    print("%s" % newDircAt)
                    self.request.sendall("SUCCESS, DIRECTORY CREATED".encode())

                except:
                    print("server could not make directory %s", request[2])
                    self.request.sendall("FAILED, DIRECTORY NOT CREATED".encode())
                # success = BaseDirectory.makeNewDirectory(request[2], "", user)

                # if success:
                # os.mkdir(request[2] + request[3])
                # self.request.sendall("SUCCESS, DIRECTORY WAS CREATED")

                # else:
                # self.request.sendall("ERROR, INCORRECT NAME OR PATH")

                # return

            # Try WRITE new file
            elif request[1] == "F":

                success = BaseDirectory.makeNewFile(request[2], request[3], user)

                if success:
                    file = open(request[2] + "", "x")
                    file.close()

                else:
                    self.request.sendall("ERROR, INCORRECT NAME OR PATH")

                return

            # else type is invalid
            else:
                self.request.sendall("ERROR, INVALID TYPE")

        elif request[0] == "READ":
            print("Server WRITE not implemented / TESTED")

        elif request[0] == "LIST":
            print("Server WRITE not implemented / TESTED")

        elif request[0] == "CREATE":
            print("Server WRITE not implemented / TESTED")

        elif request[0] == "CHANGE_PERMISSION":
            print("Server WRITE not implemented / TESTED")

        else:
            print("Error: <%s> REQUEST <%s> NOT FOUND" % (user, request))
            self.request.sendall("ERROR, NOT FOUND")

        return

    # Get the size of the next message in BYTES
    def receiveALL(self):

        totalData = ""

        while True:

            # Try to recv
            try:
                data = self.request.recv(1024).decode()

                # Join data
                if data:
                    totalData.join(data)

                else:

                    # sleep for sometime to indicate a gap
                    time.sleep(0.1)

            # Break if no more data
            except:
                pass

            return totalData




##############################################################################
class User:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.accessFiles = []
        self.accessDirectory = []
        self.ownerFiles = []
        self.ownerDirectory = []


class Directory:

    def __init__(self, name, owner, path, read, write, delete, rename):
        # directory information
        self.name = name
        self.owner = owner
        self.path = path

        # directory permissions
        self.read = read
        self.write = write
        self.delete = delete
        self.rename = rename


class File:

    def __init__(self, name, owner, path, read, write, delete, rename):
        # file information
        self.name = name
        self.owner = owner
        self.path = path

        # file permissions
        self.read = read
        self.write = write
        self.delete = delete
        self.rename = rename


################################
# Non class functions
################################


def createBaseDirectory():
    global BaseDirectory

    # SYSTEM_PATH + "SEDFS_root"
    SEDFSpath = defaultSystemPath + BaseDirectory

    # Check if PATH exists
    pathExists = os.path.isdir(SEDFSpath)

    if pathExists:


        if len(SEDFSpath) > 0 and SEDFSpath[-1] == "/" or SEDFSpath[-1] == "/":
            SEDFSpath = SEDFSpath[:-1]


        os.chmod("SEDFS_root", 777)
        serverLog.info("[*] SEDFS Directory found at: %s" % SEDFSpath)
        os.rmdir(SEDFSpath)
        serverLog.info("[-] SEDFS Directory removed at: %s" % SEDFSpath)


        serverLog.info("[+] SEDFS Directory created at: %s" % SEDFSpath)

    else:
        os.makedirs(SEDFSpath)
        serverLog.info("[+] SEDFS Directory created at: %s" % SEDFSpath)

    return


# Load given User Configs
def loadUserConfig():
    file = open("userConfig.txt", mode='r')
    lines = file.readlines()
    file.close()

    for line in lines:
        # remove whitespaces, delimiters, append to authorizedUsers
        line = line.strip()
        user = line.split(',')

        # Create User Object and Append to "authorizedUsers"
        userObject = User(user[0], user[1])
        authorizedUsers.append(userObject)
        serverLog.info("[+] New User added: %s" % user[0])




# Load given Directory Configs
def loadDirectoryConfig():
    global BaseDirectory

    file = open("directoryConfig.txt", mode='r')
    lines = file.readlines()
    file.close()

    for line in lines:

        # remove whitespaces, delimiters, append to authorizedUsers
        line = line.strip()
        directory = line.split(',')

        # Error Checking
        if len(directory) != 3:
            print("Error: Loaded directory is missing requirements")
            continue

        user = directory[0]
        name = directory[1]
        path = defaultSystemPath + BaseDirectory + directory[2]

        # Create User Object and Append to "authorizedUsers"
        directoryObject = Directory(name, user, path, True, True, True, True)

        # Search authorizedUser for OWNER
        i = 0
        while i < len(authorizedUsers):

            # In User Class, append ownerDirectory
            if authorizedUsers[i] == directoryObject.owner:
                authorizedUsers[i].ownerDirectory.append()
                os.mkdir(path)
                serverLog.info("[+] Server loaded NEW directory\tUser: %s\tName:%s\tPath%s"
                               % (user, name, path))

        # Else OWNER does not exist
        print("Error, OWNER: does not exist")


# Load given File Configs
def loadFileConfig():
    global BaseDirectory

    file = open("fileConfig.txt", mode='r')
    lines = file.readlines()
    file.close()

    for line in lines:

        # remove whitespaces, delimiters, append to authorizedUsers
        line = line.strip()
        insertFile = line.split(",")

        if len(insertFile) != 3:
            print("Error: Loaded file is missing requirements")
            continue

        user = insertFile[0]
        name = insertFile[1]
        path = defaultSystemPath + BaseDirectory + insertFile[2]

        # Create File Object and Append to "authorizedUsers"
        fileObject = File(name, user, path, True, True, True, True)

        # Search authorizedUser for OWNER
        i = 0
        while i < len(authorizedUsers):

            # In User Class, append ownerDirectory
            if authorizedUsers[i] == fileObject.owner:
                authorizedUsers[i].ownerFiles.append()
                open(path, "w")
                serverLog.info("[+] Server loaded NEW file\tUser: %s\tName:%s\tPath%s"
                               % (user, name, path))

        # Else OWNER does not exist
        print("Error, OWNER: does not exists")


# Main
if __name__ == '__main__':

    # If Python3 is setup, we can start server
    if OPERATE:

        # Create BaseDirectory, Load Users, Directories, Files
        createBaseDirectory()
        loadUserConfig()
        loadDirectoryConfig()
        loadFileConfig()

        """"
        # Set Server IP
        serverHost = socket.gethostname()
        serverIP = socket.gethostbyname(serverHost)

        # Make fileServer() Object, with (socket) and fileServerHandler
        startFileServer = fileServer(serverIP, fileServerHandler)

        startFileServer.serve_forever()
        """