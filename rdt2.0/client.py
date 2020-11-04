#Referenced from https://www.binarytides.com/programming-udp-sockets-in-python/

import socket    #for sockets
import sys    #for exit
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost';
port = 8888;

rcvpkt = []
#def isNAK(rcvpkt):
    #here we will see if the received packet as a negative acknowledgment
    
def rdt_rcv(rcvpkt):
    #here we will receive information back from the server regarding the status of the information delievered
    d = s.recvfrom(1024)
    reply = d[0]
    addr = d[1]
    
    print 'Server reply : ' + reply
    

def make_pkt(data):
    #let packet be an array containing: data
    packet = []
    packet.append(data)
    return packet

def udt_send(sndpkt):
    try :
        str = ''.join(sndpkt)
        #Set the whole string
        s.sendto(str, (host, port))
        
    
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
#wait for call from above
def rdt_send(data):
    #make packet
    sndpkt = make_pkt(data)
    #send packet
    udt_send(sndpkt)
    
   
    

while(1) :
    msg = raw_input('Enter message to send : ')
    rdt_send(msg)
    rdt_rcv(rcvpkt)
