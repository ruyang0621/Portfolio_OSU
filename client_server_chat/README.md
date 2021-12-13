Description: 
The program is the client of the Client/Server Chat program. The client creates a socket and connects to the server for communication.
The server creates a socket and binds to 'localhost' and port. Then the server communicates with a client through the socket. The server 
only handles one socket connection each time. It closes a socket connection once receive /q message from the client-side.