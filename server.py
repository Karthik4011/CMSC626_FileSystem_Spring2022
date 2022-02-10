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

#Used for Deleting files
import stat

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


##############################################################################
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


##############################################################################
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


##############################################################################
# Non class functions
##############################################################################

# Deletes ReadOnly Files
def remove_on_error(function, path, exec_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)
    return


# Creates SEDFS BaseDirectory
def createBaseDirectory():
    global BaseDirectory

    # SYSTEM_PATH + "SEDFS_root"
    SEDFSpath = defaultSystemPath + BaseDirectory

    # Check if PATH exists
    pathExists = os.path.isdir(SEDFSpath)

    if pathExists:

        #if len(SEDFSpath) > 0 and SEDFSpath[-1] == "/" or SEDFSpath[-1] == "/":
            #SEDFSpath = SEDFSpath[:-1]

        serverLog.info("[*] SEDFS Directory found at: %s" % SEDFSpath)

        shutil.rmtree(SEDFSpath, onerror=remove_on_error)
        serverLog.info("[-] SEDFS Directory removed at: %s" % SEDFSpath)

        os.makedirs(SEDFSpath)
        os.chmod(SEDFSpath, stat.S_IWRITE)
        serverLog.info("[+] SEDFS Directory created at: %s" % SEDFSpath)

    else:
        path = os.path.join(defaultSystemPath, BaseDirectory)
        os.mkdir(path)
        os.chmod(path, stat.S_IWRITE)
        serverLog.info("[+] SEDFS Directory created at: %s" % SEDFSpath)

    return


# Load given User Configs
def loadUserConfig():
    global BaseDirectory

    try:
        file = open("userConfig.txt", mode='r')
    except:
        serverLog.info("[*] userconfifConfig.txt, file not found")
        return

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

    return


# Load given Directory Configs
def loadDirectoryConfig():
    global BaseDirectory

    try:
        file = open("directoryConfig.txt", mode='r')
    except:
        serverLog.info("[*] directoryConfig.txt, file not found")
        return
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
        path = BaseDirectory + directory[2]
        #print("Test, in loadDirctoryPath path: %s" %path)

        # Create User Object and Append to "authorizedUsers"
        directoryObject = Directory(name, user, path, True, True, True, True)

        # Search authorizedUser for OWNER
        i = 0
        while i < len(authorizedUsers):

            # In User Class, append ownerDirectory
            if authorizedUsers[i].name == directoryObject.owner:
                authorizedUsers[i].ownerDirectory.append(directoryObject)
                os.mkdir(path)
                serverLog.info("[+] " + user + ", New directory add: " + BaseDirectory + directory[2])
            i += 1

        # Else OWNER does not exist
        if i > len(authorizedUsers):
            print("Error, OWNER: does not exist")


# Load given File Configs
def loadFileConfig():
    global BaseDirectory

    try:
        file = open("fileConfig.txt", mode='r')
    except:
        serverLog.info("[*] fileConfig.txt, file not found")
        return
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
        path = BaseDirectory + insertFile[2]

        # Create File Object and Append to "authorizedUsers"
        fileObject = File(name, user, path, True, True, True, True)

        # Search authorizedUser for OWNER
        i = 0
        while i < len(authorizedUsers):

            # In User Class, append ownerDirectory
            if authorizedUsers[i].name == fileObject.owner:
                authorizedUsers[i].ownerFiles.append(fileObject)
                open(path, "w")
                serverLog.info("[+] " + user + ", New file add: " + BaseDirectory + insertFile[2])

            i += 1

        # Else OWNER does not exist
        if i > len(authorizedUsers):
            print("Error, OWNER: does not exists")


def printUserPermissions():

    for i in authorizedUsers:

        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("User: %s" %i.name)
        print("Files owned:")
        for files in i.ownerFiles:
            print("\t", files.path)

        print("\nDirectories Owned:")
        for directories in i.ownerDirectory:
            print("\t", directories.path)

        print("\nOther File Permissions:")
        for extraFiles in i.accessFiles:
            print("\t", extraFiles.path)
            print("\t\tRead: %s\n\t\tWrite: %s\n\t\tDelete: %s\n\t\tRename: %s"
                  %( extraFiles.read, extraFiles.write, extraFiles.delete, extraFiles.rename))

        print("\nOther Directories Permissions:")
        for extraDirectory in i.accessDirectory:
            print("\t", extraDirectory.path)
            print("\tRead: %s\n\tWrite: %s\n\t\tDelete: %s\n\t\tRename: %s"
            % (extraDirectory.read, extraDirectory.write, extraDirectory.delete, extraDirectory.rename))
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


def updateDirectoryPermissions(listOfUsers, path, owner, name):





    for auth in authorizedUsers:

        y = 0
        while y < len(listOfUsers):

            if auth.name == listOfUsers[y]:

                directoryObject = Directory(name, owner, path, list)
                auth.accessDirectory.append(path)

            y += 5

# Load permissions for Users
def loadPermissionConfig():
    global BaseDirectory

    try:
        file = open("permissionConfig.txt", mode='r')
    except:
        serverLog.info("[*] permissionConfig.txt, file not found")
        return

    lines = file.readlines()
    file.close()

    print("Before Lines")
    for line in lines:

        # remove whitespaces, delimiters, append to authorizedUsers
        line = line.strip()
        permissionList = line.split(",")

        if len(line) < 8:
            print("Error: Loaded file is missing requirements")
            continue

        print("Length of split", len(permissionList))
        owner = permissionList[3]
        objectType = permissionList[2]
        path = permissionList[1]
        name = permissionList[0]

        permissionList = permissionList[4:]

        print("Seaching auth users")
        # Search existing users
        for i in authorizedUsers:

            # OWNER matches existing users
            if i.name == owner:

                # Search OWNER files
                if objectType == "f":
                    for files in i.ownerFiles:

                        # file match
                        if files.path == path:

                            print("Test, file match")

                            temporaryFiles = []
                            whogetsFile = []
                            z = 0
                            while z < len(permissionList):

                                temporaryFiles.append(File(name, owner, path,
                                                           permissionList[z+1],
                                                           permissionList[z+2],
                                                           permissionList[z+3],
                                                           permissionList[z+4]))

                                whogetsFile.append(permissionList[z])
                                z += 5

                            for allUsers in authorizedUsers:
                                for toAppend in whogetsFile:
                                    if allUsers.name == toAppend:
                                        allUsers.accessFiles.append(temporaryFiles[0])
                                        temporaryFiles.pop(0)
                                        break

                            print("ugh")

                        else:
                            print("Filepath does not exist: " + defaultSystemPath + path)

                elif objectType == "d":
                    print("Ugh")

                else:
                    print("Invalid objectType for permission settings")

# Main
if __name__ == '__main__':

    # If Python3 is setup, we can start server
    if OPERATE:

        # Create BaseDirectory, Load Users, Directories, Files
        createBaseDirectory()
        loadUserConfig()
        loadDirectoryConfig()
        loadFileConfig()
        
        loadPermissionConfig()
        printUserPermissions()


        """"
        # Set Server IP
        serverHost = socket.gethostname()
        serverIP = socket.gethostbyname(serverHost)

        # Make fileServer() Object, with (socket) and fileServerHandler
        startFileServer = fileServer(serverIP, fileServerHandler)

        startFileServer.serve_forever()
        """