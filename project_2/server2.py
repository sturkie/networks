import socket
import sys
from thread import *
import time
import select

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
userpass = [["cool_user","password"],["user2000","1234"],["student","cs164"]]
groups = [[],[]] #contains the users ids
usernames = ["cool_user", "user2000", "student"]
#cool_user id = 1
#user2000 id = 2
#student id = 3
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
    
    #print "this is a tuple %s" % (rcv_msg,)
    if rcv_msg in userpass:
        user = userpass.index(rcv_msg)
        
        print '"' + usernames[user] + '" has logged in'
        print 'This is user value: ' + str(user)

        
        try :
            print 'Sending valid...'
            conn.sendall('valid')
        except socket.error:
            print 'Send failed'
            sys.exit()
            
        '''
        Part-2:TODO:
        After the user logs in, check the unread message for this user.
        Return the number of unread messages to this user.
        '''
        conn.sendall('You have ' + str(len(messages[user])) + ' new messages')

        # Tips: Infinite loop so that function do not terminate and thread do not end.
        while True:
            try :
                option = conn.recv(1024)
            except:
                break
            if option == str(1):
                print 'user  is logging out...'
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

                print "This is userpass[user] %s" % (userpass[user],)
                
                #doesn't work, try to ask
                #send a sucess msg back to client
                conn.sendall('done')
            elif option == str(3):
                while True:
                    try:
                        second_option = conn.recv(1024)
                    except:
                        break
                    if second_option == str(1):
                        '''
                        Part-2:TODO: Send private message
                        '''
                        pmsg = conn.recv(1024)
                        print 'Got pmsg: ' + str(pmsg)
                        
                        rcv_id = conn.recv(1024)
                        print 'Got rcv_id: ' + str(rcv_id)
                        
                        #add psgm to message buffer
                        print 'Adding pmsg to messages[]'
                        messages[int(rcv_id)-1].append('From ' + usernames[user] + ': ' + pmsg)

                        #now do the magic
                        #send this message to the correct user's message queue
                        
                        
                    elif second_option == str(2):
                        '''
                        Part-2:TODO: Send broadcast message
                        '''
                        bmsg = conn.recv(1024)
                        print 'Got bmsg: ' + str(bmsg)

                        bmsg = 'Broadcast from "' + usernames[user] + '": ' + bmsg
                        #send msg to all connected users
                        broadcast(bmsg)
                        
                    elif second_option == str(3):
                        '''
                        Part-2:TODO: Send group message
                        '''
                        gmsg = conn.recv(1024)
                        if gmsg == str(3):
                            gmsg = conn.recv(1024)
                        print 'Got gmsg: ' + str(gmsg)

                        g_id = conn.recv(1024)
                        print 'Got g_id: ' + str(g_id)
                        
                        gmsg = 'Group #' + str(g_id) +': Message from: ' + usernames[user] + ': ' + gmsg
                        
                        #send to all members of that group
                        for id in groups[int(g_id)-1]:
                            messages[id-1].append(gmsg)
                        
            elif option == str(4):
                '''
                Part-2:TODO: Join/Quit group
                '''
                #group_choice = conn.recv(1024)
                g_opt = conn.recv(1024)

                if g_opt == str(1): #Join
                    group_num = conn.recv(1024)
                    groups[int(group_num)-1].append(user+1)
                    print '"' + usernames[user] + '"' + ' has been added to group ' + str(group_num)
                elif g_opt == str(2): #quit
                    groups[int(group_num)-1].remove(user+1)
                    print '"' + usernames[user] + '" has left the group'
                #group_num = conn.recv(1024)
                #if usernames[user] in groups[int(group_num)-1]:
                #    groups[int(group_num)-1].remove(user+1)
                #    print '"' + usernames[user] + '" has left the group'
                #    conn.sendall('left')
                #else:
                #    #group_num = conn.recv(1024)
                #    groups[int(group_num)-1].append(user+1)
                #    print '"' +  usernames[user] + '"' + ' has been added to group ' + str(group_num)
                    #conn.sendall('join')
            elif option == str(5):
                '''
                Part-2:TODO: Read offline message
                '''
                print 'Sending ' + str(len(messages[user])) + ' messages'
                conn.sendall('msg#' + str(messages[user]))

                    #Send messages from the list
                    #for item in messages:
                    #    con.sendall(item[0])
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

def broadcast(msg):
    for client in clients:
        client.send(msg)

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
        usernames.append(user)
        messages.append([])
        subscriptions.append([])
        print 'User created'
    elif message == 'listgroup':
        '''
        Part-2:TODO: Implement the functionality to list all the available groups
        '''
s.close()
