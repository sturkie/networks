# Project: Mini-Social Networking Website

In this project, we use mininet to emulate a network topology of one server node, two switch nodes, and three client nodes to recreate a miniature social networking application on top of this topology using a client-server model.
The client runs client2.py to log-in and use the features implemented. The server is responsible for authenticating its users, receive user actions and respond appropriately.

This application is run on mininet. To run the program, the command `sudo mn --custom finalTopol.py --topo mytopo -x` is used to open external terminals for each node. To test if the connection is set up correctly, use `pingall`.

The following is the network toplogy:

![topology](https://github.com/sturkie/networks/blob/master/project_2/img/topology.png)

## Client Log-in
Once the client successfully connects to the server, the user is prompted to log-in. There are 3 user log-ins hardcoded in the server file (server2.py).

Each user has a unique ID, username, and password.

![usertable](https://github.com/sturkie/networks/blob/master/project_2/img/usertable.png)

cool_user logs in and is alerted of any new messages received while offline. They are prompted with the main menu which consists of 5 different options.

![mainmenu](https://github.com/sturkie/networks/blob/master/project_2/img/prompt.png)

## Sending a Private Message

cool_user decides to send a message and inputs "3" for "Send messages". The user is prompted with a sub-menu of messaging options: Private, Broadcast, and Group.

cool_user decides to send a private message to another user. The user inputs their message and inputs the user's ID (user2000 has ID = 2).

![sendmsg](https://github.com/sturkie/networks/blob/master/project_2/img/user1sendmsg.png)

## Viewing a New Message
user2000 decides to log-in. After the second user has logged in, they are alerted that they have 1 new message. The user inputs "5" for "View messages" and see's cool_user's message.

![user2000](https://github.com/sturkie/networks/blob/master/project_2/img/user2000login.png)

## Broadcast Message
Broadcasting a message sends the message contents to all users actively connected to the server. 

The second user, user2000, decides to send a broadcast message. The first user, cool_user, is still connected to the server and receives user2000's broadcast message.

![sendbroadcast](https://github.com/sturkie/networks/blob/master/project_2/img/sendbroadcast.png)

![seebroadcast](https://github.com/sturkie/networks/blob/master/project_2/img/seebroadcast.png)

## Group Configuration

A user can create a group with other users. The user selects "4" for "Group configuration" and decides to join a group or quit a group. 

If a user decides to join a group, they have to input which group # they want to join. This information is sent to the server and the user now joins the group.

If a user decides to quit a group, they have to input which group # they want to leave that they are already joined in. 

Now the user can send group messages to all users in the group under the "Send message" menu.

## Final Notes
There are errors in the group configuration when leaving a group. A fix would be to implement a safety check to see if they are already in the group or if they try to leave a group the user never joined.

There are errors given on the server side of certain messages, such as error with the input.
