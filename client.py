import socket

# Class to Setup Client Object
class ClientInfo():
    def __init__(self):

        # Keeps track of known server port
        self.knownServerPort = 50000

        # Keeps track of known server IP address
        self.knownServerIPs = []


if __name__ == '__main__':
    print('Client is up\n')
