#fROM ARTICLE
#socket client exmaple in python
import socket #for sockets
import sys #for exit


#create an AF_INET, Stream socket by TCP
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#print 'Socket Created...'

#handles errors
try:
	#create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#print 'Socket Created...'

except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

print 'Socket Created...'


#be sure to change resolv.conf file or else it will fail!
#host = 'server.sarah.cs164'
host = 'www.google.com'
host = 'en.wikipedia.org'
port = 80
#port = 7743 #861287743


try:
	remote_ip = socket.gethostbyname(host)

except socket.gaierror:
	#could no resolve
	print 'Host name not resolved. Exiting'
	sys.exit()

print 'IP address of ' + host + ' is ' + remote_ip

#connecting to remote server
s.connect((remote_ip, port))

print 'Socket Connected to ' + host + ' on IP: ' + remote_ip

#sending data to remote server
message = "GET / HTTP/1.1\r\n\r\n"

try:
	#set whole string
	s.sendall(message)
except socket.error:
	#send failed
	print 'Send failed'
	sys.exit()

print 'Message sent successfully'

#now receive data
reply = s.recv(4096)

print reply

s.close()
print 'Socket closed.'
