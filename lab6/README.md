# Lab 6

## SCENARIO 1:
Running the server.py file then the client.py file will show a normal, functioning GBN protocol example.

Upon startup, the sender (client) sends four packets from the window to the receiver (server). The receiver outputs a response upon receiving a packet with its sequence number. Then it sends an ACK back to the sender.
The sender in the meantime waits for the ACK and start the timer after it sent the packets. It outputs the reply message from the receiver, update the base, and after it receives an acknowledgement for all 4 packets, it shifts the window and send the next four.

### Client sending Packets[0-3]
![send](https://github.com/sturkie/networks/blob/master/lab6/img/clientsend.png)


### Client receiving ACKs from receiver
![ACK](https://github.com/sturkie/networks/blob/master/lab6/img/clientreceive.png)

In normal circumstances, the server outputs a series of messages to inform what has been received.


![received](https://github.com/sturkie/networks/blob/master/lab6/img/serveroutput.png)

## SCENARIO 2:
Running the dropped_server.py then the client.py file will show what happens when the server drops a packet file.
	
The packet file that is dropped in dropped_server.py is different each time. The packet lost depends on the random value generated in receive(sock).

If a server packet is lost, the client timeouts while waiting for a packet that never made it. It resends the four packets in the window again and then the program concludes normally.

### The receiver drops packets[4] and packets[6]
![lost](https://github.com/sturkie/networks/blob/master/lab6/img/servererror.png)


Sequence numbers are always one index behind the message number.

![seqnum](https://github.com/sturkie/networks/blob/master/lab6/img/seqnum.png)

The sender waits for the responses for packets[4] and packets[6], but never receives them thus times out. Sender resends the four packets in the window again.



