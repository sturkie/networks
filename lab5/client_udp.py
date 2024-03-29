from socket import timeout
import socket
import sys
import time
from check import ip_checksum
import random

#create dgram udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()

host = 'localhost';
port = 7743;

s.settimeout(1)
seq = 0


def udt_send(sndpkt):
	msg = 'Message #' + sndpkt(i)
	checksum = ip_checksum(sndpkt)
	error = random.random()

	#set the whole string
	#s.sendto(str(seq)+' '+msg,(host,port))
	s.sendto(str(seq)+' '+msg + '' + checksum,(host,port))
	print 'Sent: ', str(seq),' ', msg, '', checksum
	try:
		#receive data from client (data, addr)
		d = s.recvfrom(1024)
		reply = d[0]
		addr = d[1]
	
		#print 'Server reply: ' + reply
		if d[0].startswith('ACK'):
			seq = 1 - seq

	except socket.error, msg:
		print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	except timeout:
		print 'Timeout'

def rdt_send(data):
    sndpkt = make_pkt(0, data, checksum)
    udt_send(sndpkt)
    start_timer
    
while(1):
    data = raw_input('Enter message to send : ')
    rdt_send(data)
