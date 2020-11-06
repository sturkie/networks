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
except socket.error, errormsg :
    print 'Failed to create socket. Error Code : ' + str(errormsg[0]) + ' Message ' + errormsg[1]
    sys.exit()


# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , errormsg:
    print 'Bind failed. Error Code : ' + str(errormsg[0]) + ' Message ' + errormsg[1]
    sys.exit()
    
print 'Socket bind complete'


packet = []
rcvpkt = []

def has_seq0(rcvpkt):
    if '0' in seq:
        return True
        
        
    
def has_seq1(rcvpkt):
    if '1' in seq:
        return True
        

def udt_send(ACK):
    if ACK == 'ACK':
        print 'Sending ACK...'
        s.sendto('ACK for ' + data, addr)
    elif ACK == 'NAK':
        print 'Sending NAK...'
        s.sendto('NAK for ' + data, addr)
    
    return
    
    
    
def corrupt(rcvpkt):
    
    checksum2 = ip_checksum(msg)
    
    #print 'Checksum = ' + str(checksum) + ', Checksum2 = ' + checksum2
    if str(checksum) != str(checksum2):
        ACK = 'NAK'
        #print 'They are NOT the same'
        return True



def notCorrupt(rcvpkt):
    checksum2 = ip_checksum(rcvpkt[1])
    
    #print 'Checksum = ' + str(rcvpkt[2]) + ', Checksum2 = ' + checksum2
    if str(rcvpkt[2]) == str(checksum2):
        ACK = 'ACK'
        #print 'They are the same'
        return True



def deliver_data(data):
    reply = 'OK...' + rcvpkt[1]
    
    #send to rdt_rcv
    s.sendto(reply, addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + str(rcvpkt[1])
    del rcvpkt[:]



#wait for call from below
def rdt_rcv(packet):
    
    if corrupt(rcvpkt) or has_seq0(rcvpkt):
        #print 'the message is on seq 0, sending NAK'
        udt_send('NAK') #send again
    elif notCorrupt(rcvpkt) and has_seq1(rcvpkt):
        #print 'the message is clear ro reply to'
        udt_send('ACK')
        #extract(packet, data)
        deliver_data(rcvpkt)
    
    #del rcvpkt[:]
    return

#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    #d = s.recvfrom(1024)
    d = (s.recvfrom(1024))
    #d = packet[0]
    
    global addr
    global data
    global msg
    global checksum
    global seq
    
    myList = []
    
    data = d[0]
    addr = d[1]
    
    #analyze data
    if '|' in str(data):
        #index = data.find(';')
        #msg = data[0:]
        myList = data.split('|')
        seq = myList[0]
        data = myList[1]
        if ';' in str(data):
            myList2 = data.split(';')
            msg = myList2[0]
            checksum = myList2[1]
    
    #print 'Sequence: ' + str(seq) + ' Message: ' + msg + ' Checksum = ' + checksum
    
    #remake packet
    rcvpkt.append(seq)
    rcvpkt.append(msg)
    rcvpkt.append(checksum)
    rdt_rcv(packet)
    
    
s.close()
