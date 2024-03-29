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
ACK = 'ACK'

def isNAK(rcvpkt):
    if ACK == 'NAK':
        return True
    else:
        return False
    #here we will see if the received packet as a negative acknowledgment
    #NAK is received when checksum fails
    
def rdt_rcv(rcvpkt):
    #here we will receive information back from the server regarding the status of the information delievered
    rcvpkt = make_pkt(s.recvfrom(1024)) #update rcvpkt
    
    d = rcvpkt[0]
    
    
    if 'NAK for ' in d:
        ACK = 'NAK'
    elif 'ACK for ' in d:
        ACK = 'ACK'
    
    
    reply = d[0]
    addr = d[1]
    
    if 'OK...' in reply:
        print 'Server reply : ' + reply
    
    return True
    

def make_pkt(data):
    #let packet be an array containing: data
    packet = []
    packet.append(data)
    return packet

def udt_send(sndpkt):
    try :
        str = ''.join(sndpkt)
        #print 'This is str: ' + str
        checksum = ip_checksum(str)
        #Set the whole string
        s.sendto(str + ';' + checksum, (host, port))
        
    
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
#wait for call from above
def rdt_send(data):
    #make packet
    sndpkt = make_pkt(data)
    #send packet
    udt_send(sndpkt)
    
    rdt_rcv(rcvpkt)
    if rdt_rcv(rcvpkt) and isNAK(rcvpkt):
        #send again
        print 'NAK received. Resending...'
        udt_send(sndpkt)
    #else do nothing except wait

while(1) :
    msg = raw_input('Enter message to send : ')
    rdt_send(msg)
    #rdt_rcv(rcvpkt)
