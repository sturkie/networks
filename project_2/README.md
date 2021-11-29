# Project: Mini-Social Networking Website

In this project, we use mininet to emulate a network topology of one server node, two switch nodes, and three client nodes to recreate a miniature social networking application on top of this topology using a client-server model.
The client runs client2.py to log-in and use the features implemented. The server is responsible for authenticating its users, receive user actions and respond appropriately.

This application is run on mininet. To run the program, the command `sudo mn --custom finalTopol.py --topo mytopo -x` is used to open external terminals for each node. To test if the connection is set up correctly, use `pingall`.

The following is the network toplogy:

![topology]()


