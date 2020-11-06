#Referenced from https://www.binarytides.com/programming-udp-sockets-in-python/

from socket import timeout
import socket    #for sockets
import sys    #for exit
from check import ip_checksum
import time
import random


# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost';
port = 8888;
addr = (host,port)

s.settimeout(1)

rcvpkt = []
seq = 0
ACK = 'ACK'

def isACK(rcvpkt,seqnum):
    if ACK == 'ACK' and seqnum == 0:
        seq = 1
        print 'Received ACK for seq0'
        return True
    elif ACK == 'ACK' and seqnum == 1:
        print 'Received ACK for seq1'
        return True

def isNAK(rcvpkt):
    if ACK == 'NAK':
        print 'Received NAK'
        return True
    else:
        return False
    #here we will see if the received packet as a negative acknowledgment
    #NAK is received when checksum fails
    
def rdt_rcv(rcvpkt):
    #here we will receive information back from the server regarding the status of the information delievered
    
    if 'NAK' in rcvpkt[0]:
        #print 'Received NAK'
        ACK = 'NAK'
        return True
    elif 'ACK' in rcvpkt[0]:
        #print 'Rceived ACK'
        ACK = 'ACK'
    
    d = rcvpkt[0]
    
    reply = d[0]
    addr = d[1]
    
    if 'OK...' in reply:
        print 'Server reply : ' + reply
    
    return True
    

def make_pkt(seq,data,checksum):
    #let packet be an array containing: data
    #calculate checksum here
    #str = ''.join(data)
    
    packet = []
    packet.append(seq)
    packet.append(data)
    packet.append(checksum)
    return packet

def udt_send(sndpkt):
    try :
        #seq = ''.join(sndpkt[0])
        seq = sndpkt[0]
        msg = ''.join(sndpkt[1])
        
        #false checksum
        
        #print 'This is str: ' + str
        #checksum = ip_checksum(str)
        #Set the whole string
        #print 'Sending: ' + str(seq) + '|' + msg + ';' + sndpkt[2]
        s.sendto(str(seq) + '|' + msg + ';' + str(random.random()), (host, port))
        
        #s.sendto(sndpkt,(host,port))
        
    
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
#wait for call from above
def rdt_send(data):
    seq = 0
    #compute checksum
    checksum = ip_checksum(data) #might have to make to string
    #make packet
    sndpkt = make_pkt(0,data,checksum)
    #send packet
    udt_send(sndpkt)
    
    try:
        #print 'About to receive input'
        d = s.recvfrom(1024) #update rcvpkt
        #print 'Input is: ' + d[0]
        
        rcvpkt.append(d)
        
        rdt_rcv(rcvpkt)
        rcvpkt.pop()
    except timeout:
        print 'Timeout'
        #resent
        udt_send(sndpkt)
    #rdt_rcv(rcvpkt)
    
    
    if isNAK(rcvpkt):
        #send again
        #print 'NAK received. Resending...'
        udt_send(sndpkt)
        del sndpkt[:]
    elif isACK(rcvpkt,0):
        #send again but with seq1
        #print 'ACK received. Sending sequence 1'
        sndpkt = make_pkt(1, data, checksum)
        udt_send(sndpkt)
        del sndpkt[:]
        #will receive second ACK
        
        try:
            rcvpkt.append(s.recvfrom(1024))
            rdt_rcv(rcvpkt)
            rcvpkt.pop()
            
            if isACK(rcvpkt, 1):
                try:
                    rcvpkt.append(s.recvfrom(1024))
                    #print 'Receiving: ' + str(rcvpkt[0])
                    rdt_rcv(rcvpkt)
                    rcvpkt.pop()
                except timeout:
                    print 'Timeout'
                    sndpkt = make_pkt(1, data, checksum)
                    udt_send(sndpkt)
                    del sndpkt[:]
                    #resend
        except timeout:
            sndpkt = make_pkt(1, data, checksum)
            udt_send(sndpkt)
            del sndpkt[:]
            print 'Timeout'
    #else do nothing except wait

while(1) :
    msg = raw_input('Enter message to send : ')
    rdt_send(msg)
    
