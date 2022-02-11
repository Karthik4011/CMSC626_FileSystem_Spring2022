import platform
import socket
import os
import shutil
import time

ServerPort = 50000  # server port
clientConnection = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)  # client IPv4 socket
currentSEDFSpath = "SEDFS_root/"  # Current path on SEDFS
listOfServers = []  # list of known servers
OS = platform.system()  # "Linux" or "Windows"

listOfNo = ["no", "n"]
listOfYes = ["yes", "y"]
fileOrDirectory = ["F", "D", "f", "d"]


# Display Help Menu
def help():
    print("============================\n",
          "\nCurrent Path: " + currentSEDFSpath + "\n\n"
                                                  "\t'q' == Quit SEDFS\n",
          "\t'r' == Read SEDFS file\n",
          "\t'w' == Write to the current Reading\n",
          "\t'c' == Create new file/directory\n",
          "\t'n' == Navigate to new directory\n",
          "\t'b' == Move back 1 directory\n",
          "\t'l' == List contents\n",
          "\t'd' == Delete file/directory\n",
          "\t's' == Display Server Information\n",
          "\t'h' == Help\n")


# Open Text Editor
# Gets notepad on Windows, Nano on Linux
def openTextEditor():
    if OS == "Windows":
        return shutil.which("notepad")

    elif OS == "Linux":
        return shutil.which("nano")


# arg == IP address
def connectServer():
    # Get Main Server IP and add info to Client Class
    global clientConnection

    while 1:
        print("Input SEDFS Server IPv4 Address ('quit' to exit)\n>> ", end='')
        serverIP = input().strip()

        if serverIP == "QUIT" or serverIP == "Q" or serverIP == "quit" or serverIP == "q":
            return False

        # try to make a connection
        try:
            # Set 10 second time out, Attempt connection
            clientConnection = socket.create_connection((serverIP, ServerPort), timeout=10)
            print(">> Intial Connection to %s found!" % serverIP)
            listOfServers.append(serverIP)
            return True

        except Exception as e:
            print("Could not connect to \"%s\" on port \"%s\"\nError: %s\n\n" % (serverIP, ServerPort, e))


def runningMenu():

    #change socket timeout to 30 seconds
    #clientConnection.settimeout(30)

    while 1:
        print(" >> ", end='')
        clientRequest = input().lower()

        if clientRequest == "h" or clientRequest == "help":
            help()

        elif clientRequest == "q":
            print("Quiting File Server")
            clientConnection.close()

        elif clientRequest == "r":
            # implement code to READ new file
            print("Quit Not implemented")
            # Request to READ file in "current SEDFS path"
            # Display result from server response

        elif clientRequest == "w":
            print("Write Not implemented")

        elif clientRequest == "c" or clientRequest == "create":
            create()

        elif clientRequest == "n":
            # implement code to NAVIGATE to new directory
            print("Navigate to Directory Not implemented")
            # Ask user for path request

        elif clientRequest == "b":
            # implement code to WRITE to READ file
            print("Move Back Not implemented")
            # Request server to go back one directory
            # Display server response (SUCCESS or FAILURE)
            # Display new path

        elif clientRequest == "l":
            # implement code to WRITE to READ file
            print("List Contents Not implemented")
            # Request server to list current directory contents
            # Diplay server response

        elif clientRequest == "d":
            # implement code to DELETE file/directory
            print("Delete Not implemented")
            # Ask user for file to delete
            # Send delete request to server
            # !!! Server Should Only delete directory if empty !!
            # Tell user status

        elif clientRequest == "s":
            # implement code to display server information
            print("Server Information Not implemented")
            information.clientSocket.send("SYN".encode())
            serverResponse = information.clientSocket.recv(1024).decode()
            print("Server Response: %s", serverResponse)


def sendUserNameAndPassword():
    # Get server response
    serverResponse = clientConnection.recv(1024).decode()
    print(serverResponse)

    while 1:

        # Get Username and Password
        username = input("Please enter username:\n >> ")
        password = input("Please enter password:\n >> ")

        # Combine info and send
        sendToServer = username + " " + password
        clientConnection.send(sendToServer.encode())

        # Get Server Response
        serverResponse = clientConnection.recv(1024).decode()

        if serverResponse == "LOGIN_SUCCESS":
            print(serverResponse)
            return True

        else:
            print(serverResponse)

        serverResponse = input("Try again?\n >> ").lower()

        if (serverResponse == "q" or serverResponse == "n" or
                serverResponse == "no" or serverResponse == "quit" or
                serverResponse == "exit"):
            # close connection
            closeConnection()

            return False


def closeConnection():
    print("Closing server connection")
    clientConnection.close()


def create():
    # How SEND and RECV should work

    # 1 send for command WRITE
    # 3 sends "path", "type", "name"
    # 1 recv for SUCCESS or FAIL

    new_path = ""
    # Ask if user wants new path
    while True:
        print("Would you like to enter a new path?\n>> ", end='')
        ans = input().lower()

        if ans in listOfYes or ans in listOfNo:
            break

    # Ask for new path
    if ans == "yes" or ans == "y":
        print("Enter New Path\n>> ")
        new_path = input()

    # Keep current path
    if ans == "no" or ans == "n":
        new_path = currentSEDFSpath

    while True:
        print("Directory <D> or File <F>?\n >> ", end='')
        fileOrDirc = input().upper()

        if fileOrDirc in fileOrDirectory:
            break

    print("Object Name?\n >> ", end='')
    name = input()

    clientConnection.send("WRITE".encode())
    time.sleep(0.1)
    clientConnection.send(new_path.encode())
    time.sleep(0.1)
    clientConnection.send(fileOrDirc.encode())
    time.sleep(0.1)
    clientConnection.send(name.encode())

    serverResponse = clientConnection.recv(1024).decode()

    print(serverResponse)


# Main
if __name__ == '__main__':

    # Initial server connection
    ifConnected = connectServer()

    # if connected
    if ifConnected:

        # attempt login
        loginSuccess = sendUserNameAndPassword()

        # if successful login
        if loginSuccess:
            # print menu
            help()
            runningMenu()

            # close connection
            closeConnection()

""""
    while not intialConnection:
        print("Reattempt server connection?\n>> ", end='')
        clientRequest = input().lower()

        if clientRequest == "n" or clientRequest == "no":
            print("Quiting client application without server connection")
            clientRequest = 'q'
            break

        elif clientRequest == "y" or clientRequest == "yes":
            intialConnection = connectServer(information)

    # Enter Username and Password
    if clientRequest != 'q':
        
        information.clientSocket.send(username.encode())
        serverResponse = information.clientSocket.recv(1024).decode()

        if serverResponse == "PASSWORD":
            username = input("Please enter password:\n >>")
            information.clientSocket
            serverResponse = information.clientSocket
            if serverResponse == "LOGIN_SUCCESS":
                connected = True
            else:
                print("Unexpected Error: Server Response: %s" % serverResponse)

    # Client Menu script
    if connected:
        while connected:
            print("n>> Current SEDFS Path: %s\n>> " % currentSEDFSpath, end='')

            

            # Clear Screen
            # os.system('cls' if os.name == 'nt' else 'clear')

"""
