import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
    s=""
    for item in t:
        s = s + str(item) + "<>"
    return s[:-2]

def stringToTuple(s):
    t = s.split("<>")
    return t

'''
Create Socket
'''
HOST = ''    # Symbolic name meaning all available interfaces
PORT = 9486    # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'

'''
Define variables:
username && passwd
message queue for each user
'''
clients = []
# TODO: Part-1 : create a var to store username && password. NOTE: A set of username/password pairs are hardcoded here.
# e.g. userpass = [......]
userpass = [["cool_user","password"],["user2000","1234"]]
messages = [[],[],[]]
count = 0

'''
Function for handling connections. This will be used to create threads
'''
def clientThread(conn):
    global clients
    global count
    # Tips: Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    rcv_msg = conn.recv(1024)
    rcv_msg = stringToTuple(rcv_msg)
    
    print "this is a tuple %s" % (rcv_msg,)
    if rcv_msg in userpass:
        user = userpass.index(rcv_msg)
        
        try :
            print 'Sending valid...'
            conn.sendall('valid')
        except socket.error:
            print 'Send failed'
            sys.exit()
            
        # Tips: Infinite loop so that function do not terminate and thread do not end.
        while True:
            try :
                option = conn.recv(1024)
            except:
                break
            if option == str(1):
                print 'user  is logging out...'
                # TODO: Part-1: Add the logout processing here
                break

            elif option == str(2):
                print 'Change password'

                #receiving new login credentials
                rcv_msg = conn.recv(1024)
                
                rcv_msg = stringToTuple(rcv_msg)
                print 'Received new password'

                #print "This is the new login %s" % (rcv_msg,)

                #update userpass
                userpass[user] = rcv_msg

                print "This is userpass[user] %s" % (userpass[0],)
                
                #doesn't work, try to ask
                #send a sucess msg back to client
                #conn.sendall('done')
            else:
                try :
                    conn.sendall('Option not valid')
                except socket.error:
                    print 'option not valid Send failed'
                    conn.close()
                    clients.remove(conn)
    else:
        try :
            conn.sendall('nalid')
        except socket.error:
            print 'nalid Send failed'
    print 'Logged out'
    conn.close()
    if conn in clients:
        clients.remove(conn)

def receiveClients(s):
    global clients
    while 1:
        # Tips: Wait to accept a new connection (client) - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        clients.append(conn)
        # Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientThread ,(conn,))

start_new_thread(receiveClients ,(s,))

'''
main thread of the server
print out the stats
'''
while 1:
    message = raw_input()
    if message == 'messagecount':
        print 'Since the server was opened ' + str(count) + ' messages have been sent'
    elif message == 'usercount':
        print 'There are ' + str(len(clients)) + ' current users connected'
    elif message == 'storedcount':
        print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
    elif message == 'newuser':
        user = raw_input('User:\n')
        password = raw_input('Password:')
        userpass.append([user, password])
        messages.append([])
        subscriptions.append([])
        print 'User created'
s.close()
