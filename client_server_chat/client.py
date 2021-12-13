# Author: Ru Yang
# Date: 11/29/2021
# Description: The program is the client of the Client/Server Chat program. The client creates a socket and 
#              connects to the server for communication.

# Citation for the following function: Use the Python socket API to build a Client/Server Chat program.                                   
# Date: 11/29/2021

# Copied from /OR/ Adapted from /OR/ Based on: ZetCode Python Socket - Python Socket GET request
# Source URL:                                  https://zetcode.com/python/socket/

# Copied from /OR/ Adapted from /OR/ Based on: stackOverflow - python socket GET 
# Source URL:                                  https://stackoverflow.com/questions/34192093/python-socket-get

# Copied from /OR/ Adapted from /OR/ Based on: Simple Server and Client Chat using Python by Ashok Kumar
# Source URL:                                  https://www.biob.in/2018/04/simple-server-and-client-chat-using.html

import sys
from socket import *

# Declare the host and port.
# Declare the host and port.
HOST = 'localhost'
PORT = 7002

"""
Create a socket by using socket method. 
Address family AF_INET is Internet Protocol v4 addresses. 
SOCK_STREAM means that it is a TCP socket.
"""
clientSocket = socket(AF_INET, SOCK_STREAM)

# Give HOST address and PORT number to the socket,
clientSocket.connect((HOST, PORT))
print("Connected to: %s on port: %d" % (HOST, PORT))

# Prompt input
print('Type /q to quit')
print('Enter message to send...')
while True:
    msgSent = input(str(">"))
    clientSocket.send(msgSent.encode())

    # Break if "/q" enter
    if msgSent == "/q":
        break

    # Print receive message
    msgRecv = clientSocket.recv(1024).decode()
    print(msgRecv)
    
    # Break if receive"/q" 
    if msgRecv == "/q":
        break

# Close the socket.
clientSocket.close()
