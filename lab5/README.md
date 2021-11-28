# Lab 5
## Non-corrupt Sending
The user enters a message and the message is sent in a packet with sequence number = 0, the message itself, and checksum.
![send](https://github.com/sturkie/networks/blob/master/lab5/img/sendmsg.png)

Server sends a NAK since sequence number is 0. Once the sender receives the NAK it resends the message with a sequence number = 1.
The receiver now sends an ACK signal back to the sender.
![server](https://github.com/sturkie/networks/blob/master/lab5/img/receiverack.png)

Upon receiving the ACK signal from the receiver, the sender also receives the server reply and output. Meanwhile the receiver outputs the sender’s message.

## Timeout
The sender timeouts if it is unable to receive an ACK/NAK from the receiver in a set amount of time. Upon timeout, the sender resends its original message to the receiver in an attempt to receive a response.

![timeout](https://github.com/sturkie/networks/blob/master/lab5/img/timeout.png)

NOTE: This code is incorrect because the sender is unable to recognize the receiver’s NAK response, so it will timeout with no successful attempt of recovery from the resend.

## Checksum

The sender and receiver must both calculate the same checksum of a message in order to ensure that the message received is the same as the one sent. If the calculated checksum differs, the receiver sends NAKs to the sender alerting it of an error. The sender then resends the message in an attempt to achieve checksum success.

![checksum](https://github.com/sturkie/networks/blob/master/lab5/img/checksum.png)
![NAK](https://github.com/sturkie/networks/blob/master/lab5/img/nak.png)

NOTE: This program is incorrect because the sender is unable to properly recognize the receiver’s NAK response. Also, since the checksum is purposely incorrect, it won’t ever be corrected. However, in the original code the error would correct itself upon a packet resend.

## Errors
In order to simulate a timeout error and checksum error, the checksum is hard coded to a ‘false’ variable and the timeout is done by making the sender think it never received any type of acknowledgement from the receiver.



