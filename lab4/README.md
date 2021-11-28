# Lab 4
The goal of this lab is to begin socket programming in Python. Here we first open a server application where it waits and listens. We establish two connections by the telnet protocol.

### Initial execution of server.py
![open](https://github.com/sturkie/networks/blob/master/lab4/img/serveropen.png)

### First telnet connection from mininet
![firstconnection](https://github.com/sturkie/networks/blob/master/lab4/img/firstconnection.png)

### Second telnet connection from mininet
![secondconnection](https://github.com/sturkie/networks/blob/master/lab4/img/secondconnection.png)

From the second connection, we use `!sendall <msg>` to send "Hello from second connection" to all currently connected clients. The first connection we made receives the message.

### Second connection sends a message
![sendall](https://github.com/sturkie/networks/blob/master/lab4/img/sendall.png)

### First connection perspective
![firstconnection](https://github.com/sturkie/networks/blob/master/lab4/img/firstconnectionsendall.png)

We close the first connection using `!q`. All updates are seen from the server perspective (sendall, quit).

### First connection closes
![quit](https://github.com/sturkie/networks/blob/master/lab4/img/quit.png)

### Server perspective
![close](https://github.com/sturkie/networks/blob/master/lab4/img/serverclose.png)
