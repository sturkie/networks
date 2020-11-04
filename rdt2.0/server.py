#Referenced from https://www.binarytides.com/programming-udp-sockets-in-python/

import socket
import sys
from check import ip_checksum

HOST = ''    # Symbolic name meaning all available interfaces
PORT = 8888    # Arbitrary non-privileged port

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()


# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
    
print 'Socket bind complete'


packet = []


def udt_send(ACK):
    if ACK == 'ACK':
        s.sendto('ACK for ' + data, addr)
    elif ACK == 'NAK':
        s.sendto('NAK for ' + data, addr)
    
def corrupt(rcvpkt):
    d = rcvpkt[0]
    
    checksum2 = ip_checksum(msg)
    
    #print 'Checksum = ' + checksum + ', Checksum2 = ' + checksum2
    if str(checksum) == str(checksum2):
        ACK = 'ACK'
    elif str(checksum) != str(checksum2):
        ACK = 'NAK'
        
    udt_send(ACK)


def deliver_data(data):
    reply = 'OK...' + msg
    
    #send to rdt_rcv
    s.sendto(reply, addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + msg.strip()

#wait for call from below
def rdt_rcv(packet):
    #d = s.recvfrom(1024)
    packet.append(s.recvfrom(1024))
    d = packet[0]
    
    global addr
    global data
    global msg
    global checksum
    
    myList = []
    
    data = d[0]
    addr = d[1]
    if ';' in str(data):
        #index = data.find(';')
        #msg = data[0:]
        myList = data.split(';')
        msg = myList[0]
        checksum = myList[1]
    
    corrupt(packet)


    #extract(packet, data)
    deliver_data(data)
    packet.pop()

#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    
    rdt_rcv(packet)
    
    
s.close()
