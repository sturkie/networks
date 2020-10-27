import socket
import sys
from thread import *

HOST = '' # symbolic name meaning all available interfaces
PORT = 7743 # SID 861287743

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error code: ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'

#listen for incoming connections
#10 connections are waiting to be processed, the 11th connection request shall be rejected
s.listen(10)
print 'Socket listening'

close_str = "!q"
sendall_msg = "!sendall"

#a list of clients
clients = []
#clients_lock = threading.Lock() #?

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n')

	global clients
	clients += [conn]
	#infinite loop so that function does not terminate and thread does not end
	
	while True:
			#receiving from client
		data = conn.recv(1024)
		reply = 'OK ...' + data
		if close_str in str(data):
			print 'Closing connection'
			break
		if sendall_msg in str(data):
			print 'Sending to all'
			sendall(data[(len(sendall_msg)):])
		else:
			conn.sendall(reply)
		if not data:
			break
	conn.close()

#new function to output to all
def sendall(message):
	for client in clients:
		client.send(message)
#stay connected
while 1:

	#accept connection
	conn, addr = s.accept()

	#display client information
	print 'Connected with ' + addr[0] + ': ' + str(addr[1])

	#start new thread; takes 1st argument as a function name to be run, second is the tuple of arguments to the function
	start_new_thread(clientthread ,(conn,))
s.close()
