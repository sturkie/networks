# Project: Mini-Social Networking Website

In this project, we use mininet to emulate a network topology of one server node, two switch nodes, and three client nodes to recreate a miniature social networking application on top of this topology using a client-server model.
The client runs client2.py to log-in and use the features implemented. The server is responsible for authenticating its users, receive user actions and respond appropriately.

This application is run on mininet. To run the program, the command `sudo mn --custom finalTopol.py --topo mytopo -x` is used to open external terminals for each node. To test if the connection is set up correctly, use `pingall`.

The following is the network toplogy:

![topology]()

## Client Log-in
Once the client successfully connects to the server, the user is prompted to log-in. There are 3 user log-ins hardcoded in the server file (server2.py).

Each user has a unique ID, username, and password.

![usertable]()

cool_user logs in and is alerted of any new messages received while offline. They are prompted with the main menu which consists of 5 different options.

![mainmenu]()

## Sending a Private Message

cool_user decides to send a message and inputs "3" for "Send messages". The user is prompted with a sub-menu of messaging options: Private, Broadcast, and Group.

cool_user decides to send a private message to another user. The user inputs their message and inputs the user's ID (user2000 has ID = 2).

![sendmsg]()

## Viewing a New Message


