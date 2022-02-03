import socket


# Class to Setup Client Object
class ClientInfo:
    knownServerIPs = []
    knownServerPort = 50000

    def __init__(self):
        return


if __name__ == '__main__':
    # Make Client Class
    information = ClientInfo

    # Get Main Server IP and add info to Client Class
    print('Input SEDFS Server IPv4 Address\n>>', end='')
    serverIP = input().strip()
    information.knownServerIPs.append(serverIP)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((information.knownServerIPs[0], information.knownServerPort))
    clientSocket.send("TEST")
    response = clientSocket.recv(1024)
    print("\n>> %s" % response, end='')
