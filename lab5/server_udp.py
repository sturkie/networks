import socket
import sys
import time
from check import ip_checksum
import random

HOST = ''
PORT = 7743 #861287743

#UDP socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

#Bind socket to local host and port
try:
	s.bind((HOST,PORT))
except socket.error, msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'

#keep talking w client
def deliver_data(data):
	#receive data from client (data,addr)
	d = data[0]
	addr = data[1]
    seq=data[0]
    msg=data[2:12]
    checksum=data[12:]
    checksum2=ip_checksum(msg)
    print seq, '-', msg, ' , checksum= ', checksum, ' from ', addr

	if not data:
		break
	
    delay=random.random()*2
    time.sleep(delay)
 
	#reply = 'OK . . . ' + data

    if str(expecting)==str(seq) and str(checksum)==str(checksum2):
        s.sendto('ACK for ' + data[0], data[1])
        expecting = 1 - expecting

	#s.sendto(reply, addr)
	#print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

def rdt_recv(revpkt):
    extract(revpkt,data)
    deliver_data(data)
    
while 1:
    revpkt = s.recvfrom(1024)
    rdt_recv(revpkt)

s.close()
