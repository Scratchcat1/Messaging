# Messaging
A very basic messaging system for python with a GUI and a server.  
Sockets is the server, tkinter GUI is the user end.  
The IP is coded into the user end program. The user connects to the server and can log in or create a new user. If either fails it is disconnected and should automatically reconnect. Once logged in the user can create groups, send messages and delete users.
Currently isn't particularly useful or stable, will crash if too many messages are sent at once with a parsing error. Therefore one must add a system to send messages one by one or check if messages have been sent.
