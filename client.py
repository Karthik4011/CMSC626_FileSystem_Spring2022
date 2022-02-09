import socket
import os


# Class to Setup Client Object
class ClientInfo():
    knownServerIPs = []
    knownServerPort = 50000
    clientSocket = None

    def __int__(self):
        pass

    def makeSocket(self):
        IP = self.knownServerIPs[0]
        port = self.knownServerPort

        ### UGH!!! THIS MIGHT CAUSE ERRORS
        ## THIS might be ClientInfo. instead of self
        self.clientSocket = socket.create_connection((IP, port), timeout=10)

    def addIP(self, string):
        self.knownServerIPs.append(string)

    def popIP(self):
        self.knownServerIPs.pop()


# Display Help Menu
def help():
    print("============================\n",
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


"""
arg1: ClientInfo Class
arg2: Socket
"""

# Open Text Editor
# Gets notepad on Windows, Nano on Linux
def openTextEditor():
    if OS == "Windows":
        return shutil.which("notepad")

    elif OS == "Linux":
        return shutil.which("nano")


# arg == IP address
def connectServer(client):
    # Get Main Server IP and add info to Client Class
    print('Input SEDFS Server IPv4 Address\n>> ', end='')
    serverIP = input().strip()

    ClientInfo.addIP(client, serverIP)

    # Set 10 second time out, Attempt connection
    try:
        ClientInfo.makeSocket(client)
        print(">> Connected to server, enter command or type 'help'")
        return True

    except Exception as e:
        print("Could not connect to \"%s\" on port \"%s\"\nError: %s\n\n" % (serverIP,
                                                                             client.knownServerPort, e))
        ClientInfo.popIP(client)

    return False


# Main
if __name__ == '__main__':

    information = ClientInfo  # Hold info about Client
    clientRequest = ""  # Client -> Server Request
    currentSEDFSpath = "SEDFS_root/"  # Current path on SEDFS
    connected = False

    # Create IPv4, TCP socket
    # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Initial server connection
    intialConnection = connectServer(information)

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
        username = input("Please enter username:\n >>")
        information.clientSocket.send(username.encode())
        serverResponse = information.clientSocket.recv(1024).decode()

        if serverResponse == "PASSWORD":
            username = input("Please enter password:\n >>")
            information.clientSocket.send(username.encode())
            serverResponse = information.clientSocket.recv(1024).decode()
            if serverResponse == "LOGIN_SUCCESS":
                connected = True
            else:
                print("Unexpected Error: Server Response: %s" % serverResponse)

    # Client Menu script
    if connected:
        while connected:
            print("n>> Current SEDFS Path: %s\n>> " % currentSEDFSpath, end='')
            clientRequest = input().lower()

            # Clear Screen
            # os.system('cls' if os.name == 'nt' else 'clear')

            if clientRequest == "h" or clientRequest == "help":
                help()

            elif clientRequest == "q":
                print("Quit Not implemented")
                information.clientSocket.close()
                connected = False

            elif clientRequest == "r":
                # implement code to READ new file
                print("Quit Not implemented")
                # Request to READ file in "current SEDFS path"
                # Display result from server response

            elif clientRequest == "w":

                new_path = ""

                # implement code to WRITE file
                print("Write Not implemented")
                # Look at 'current local path' for READ file
                while True:
                    print("Would you like to enter a new path?\n>> ", end='')
                    ans = input().lower()

                    if ans == "" or ans == "no" or ans == "n" or ans == "yes" or ans == "y":
                        break

                if ans == "yes" or ans == "y":
                    new_path = input("Enter New Path\n>> ")
                    if new_path == "":
                        ans = "no"

                if ans == "no" or ans == "n":
                    total_path = currentSEDFSpath

                else:
                    total_path = new_path

                print("Directory <D> or File <F>?\n>> ", end='')
                fileOrDirc = input().upper()

                print("Object Name?\n>> ", end='')
                name = input().upper()

                clientRequest = "WRITE" + " " + fileOrDirc + " " + total_path + " " + name
                clientRequest = clientRequest.encode()
                information.clientSocket.sendall(clientRequest)
                serverResponse = information.clientSocket.recv(1024).decode()

                print(serverResponse)
                # Copy contents of READ file
                # Request server to WRITE
                # Send WRITE request
                # Send currentReadPath
                # Server responds with "GRANTED" or "NOT_VALID"

            elif clientRequest == "c":
                # implement code to CREATE file/directory
                print("Create New FILE/DIRECTORY Not implemented")

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
