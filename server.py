# Used to setup server handler
import socketserver

# Used to get serverIP
import socket

# Used to setup logging
import logging
import logging.config

# Used to display logging to stdout
import sys

# Used for Current Time
from datetime import datetime


# fileServer child Class, whose super class is socketServer.TCPServer
class fileServer(socketserver.TCPServer):

    # __init__ ("fileServer" child class)
    def __init__(self, serverIP, childHandler):
        #######################################
        # Create Unique Server Variables
        #######################################

        # Valid Users and Password
        self.authorizedUsers = ["admin", "password", "bob", "1234", "alice", "abcd"]

        # Users Online
        self.activeUsers = []

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
        print(date, end='')
        self.serverLog.debug("File Server Started")

        # Call Super Class "TCPServer", to __init__ Child TCPServer Class
        socketserver.TCPServer.__init__(self, serverIP, childHandler)
        return


# fileServerHandler child class, whose super class is socketserver.BaseRequestHandler
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
        print(datetime.now().strftime("DATE: %Y:%m:%d\tTIME: %H:%M:%S\t\tEVENT: "), end='')
        self.serverHandlerLog.info("File Handler Started")

        # Call Super Class "BaseRequestHandler", to __init__ Child Handler Class
        socketserver.BaseRequestHandler.__init__(self, requestType, clientIP, serverIP)
        return

    # NEEDED!!!
    # handle() method must be implemented to override the super class
    def handle(self):
        print("Server handler looking for connection")

        data = self.request.recv(1024)
        print("Data Received: %s" % data)

        # Split data into an array
        dataArray = data.split()

        # Send back ACK
        self.request.sendall("ACK")
        return


if __name__ == '__main__':
    # Set Server IP
    serverHost = socket.gethostname()
    serverIP = socket.gethostbyname(serverHost)

    # Set Port Number
    serverPort = 50000

    # Make fileServer() Object, with (socket) and fileServerHandler
    startFileServer = fileServer((serverIP, serverPort), fileServerHandler)

    # fileServerHandler.request.recv(1024)
    # Makes FileServer run indefinitely
    # startFileServer.serve_forever()
    # startFileServer.get_request()
