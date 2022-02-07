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
    currentREAD = ""  # Current READ file
    currentREADpath = ""  # Current READ path
    currentSEDFSpath = ""  # Current path on SEDFS

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


    # Client Menu script
    while clientRequest != 'q':
        print(">> Current Read: %s\n>> Current SEDFS Path: %s\n>> " % (currentREAD, currentSEDFSpath), end='')
        clientRequest = input().lower()

        # Clear Screen
        os.system('cls' if os.name == 'nt' else 'clear')

        if clientRequest == "h" or clientRequest == "help":
            help()

        elif clientRequest == "q":
            # implement code to break server
            print("Quit Not implemented")
            # Close TCP connection

        elif clientRequest == "r":
            # implement code to READ new file
            print("Quit Not implemented")
            # Request to READ file in "current SEDFS path"
            # Display result from server response

        elif clientRequest == "w":
            # implement code to WRITE to READ file
            print("Write Not implemented")
            # Look at 'current local path' for READ file
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
