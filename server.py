import socketserver
import socket


# Class instance to handle server requests
# Must pass "socketserver"."BaseRequestHandler" to be instantiated once per connection
class fileServerHandler(socketserver.BaseRequestHandler):

    def __init__(self):
        print('File Server is up\n')

    # NEEDED, handle() method must be implemented to override the super class
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == '__main__':
    # Set Server IP
    serverHost = socket.gethostname()
    serverIP = socket.gethostbyname(serverHost)

    # Set Port Number
    port = 50000

    fileServer = socketserver.TCPServer((serverIP, port), fileServerHandler)
    print('File Server is up\n')
