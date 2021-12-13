# Author: Ru Yang
# Date: 11/29/2021
# Description: The program is the server of the Client/Server Chat program. The server creates a socket and binds to 'localhost' and port.
#              Then the server communicates with a client through the socket. The server only handles one socket connection each time. It 
#              closes a socket connection once receive /q message from the client-side.

# Citation for the following function: Use the Python socket API to build a Client/Server Chat program.                                   
# Date: 11/29/2021

# Copied from /OR/ Adapted from /OR/ Based on: Computer Networking A Top-Down Approach 7th Edition Section 2.7 page 205 (mainly)
# Author:                                      Kurose Ross

# Copied from /OR/ Adapted from /OR/ Based on: How create HTTP-Server using python Socket by Emalsha 
# Source URL:                                  https://emalsha.wordpress.com/2016/11/22/how-create-http-server-using-python-socket/

# Copied from /OR/ Adapted from /OR/ Based on: Simple Server and Client Chat Using Python by Ashok Kumar
# Source URL:                                  https://www.biob.in/2018/04/simple-server-and-client-chat-using.html


import sys
from socket import *

# Declare the host and port.
HOST = 'localhost'
PORT = 7002

"""
Create a socket by using socket method. 
Address family AF_INET is Internet Protocol v4 addresses. 
SOCK_STREAM means that it is a TCP socket.
"""
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Give HOST address and PORT number to the socket,
serverSocket.bind((HOST, PORT))
print("Server listening on: %s on port: %d" % (HOST, PORT))

""" 
Enable the server to listen requests. Backlog argument specifies the unaccepted connections 
that the system will allow before refusing new connections.
"""
serverSocket.listen(1)

"""
When the request from client sent, the socket accept the connection.
connection is a new socket object usable to send an receive data on the connection.
address is the address bound to the socket on the other end of the connection.
"""
conn, addr = serverSocket.accept()
print('Connected by (\'%s\', %s)' %(addr[0], addr[1]))
print('Waiting for message...')

# Receive the first request from client side and then decode it.
request = conn.recv(1024).decode()

# The first request from client is not end message.
if request != "/q":
    # Print the first request.
    print(request)

    # Prompt input
    print('Type /q to quit')
    print('Enter message to send...')
    
    while True:
        message = input(str(">"))
        
        # Send the encoded response content to client.
        conn.send(message.encode())
        
        # Break if "/q" enter
        if message == "/q":
            break
        
        # Receive the request from client side and then decode it.
        request = conn.recv(1024).decode()

        # Check if "/q" enter from client, break
        if request == "/q":
            break
        
        # Print the request.
        print(request)

# Close the connection.
conn.close()
# Close the socket.
serverSocket.close()
    


