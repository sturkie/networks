from socket import timeout
import socket
import sys
import time
#from check import ip_checksum
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

def rdt_send(data)
    sndpkt = make_pkt(0, data, checksum)
    udt_send(sndpkt)
    start_timer

def udt_send(pkt)
	msg = raw_input('Enter message to send: ')

	#msg = 'Message #' + str(i)
	#checksum eventually goes here
	error = random.random()

	#set the whole string
	s.sendto(str(seq)+' '+msg,(host,port))
	#s.sendto(str(seq)+' '+msg + '' + checksum,(host,port))
	print 'Sent: ', str(seq),' ', msg
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
