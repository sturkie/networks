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


def deliever_data(data):
    reply = 'OK...' + data
    
    #send to rdt_rcv
    s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

    
#wait for call from below
def rdt_rcv(packet):
    #d = s.recvfrom(1024)
    packet.append(s.recvfrom(1024))
    d = packet[0]
    
    global addr
    global data
    
    data = d[0]
    addr = d[1]

    #extract(packet, data)
    deliever_data(data)
    packet.pop()

#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    
    rdt_rcv(packet)
    
    
s.close()
