import socket
import sys
from thread import *
import getpass
import os
import select

'''
Function Definition
'''
def receiveThread(s):
    while True:
        try:
            reply = s.recv(4096) # receive msg from server
            
            # You can add operations below once you receive msg
            # from the server

        except:
            print "Connection closed"
            break
    

def tupleToString(t):
    s = ""
    for item in t:
        s = s + str(item) + "<>"
    return s[:-2]

def stringToTuple(s):
    t = s.split("<>")
    return t

'''
Create Socket
'''
try:
    # create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = '10.0.0.4'
port = 9486
try:
    remote_ip = socket.gethostbyname(host)
except socket.gaierror:
    print 'Hostname could not be resolved. Exiting'
    sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip

'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

inputs = [s]
outputs = []
timeout = 10

readable, writable, exceptional = select.select( inputs, outputs, inputs, timeout)

'''
Receive Welcome
'''

print '\n'
welcome_msg = s.recv(1024)
print welcome_msg
print '--------------------------------'


'''
TODO: Part-1.1, 1.2:
Enter Username and Passwd
'''

username = raw_input('Enter username: ')

passwd = getpass.getpass()

# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden).
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()

# Send username && passwd to server

s.sendto(username + '<>' + passwd, (host,port))

'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side.
'''
reply = s.recv(5)
#print 'this is reply:' + reply
if reply == 'valid': # TODO: use the correct string to replace xxx here!
    # Receive number of new messages
    msg_intro =  s.recv(1024)
    print str(msg_intro)

    # Start the receiving thread
    start_new_thread(receiveThread ,(s,))

    
    message = ""
    while True :
        
        # TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
        message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Change password \n 3. Send messages \n 4.Group configuration \n 5. Offline message \n Choose:")
        try :
            # TODO: Send the selected option to the server
            s.sendto(message, (host,port))
            # HINT: use sendto()/sendall()
            if message == str(1):
                print 'Logout'
                # TODO: add logout operation
                break
            if message == str(2):
                #print 'Post a message'
                # Add other operations, e.g. change password
                curr_passwd = getpass.getpass(prompt='Enter current password: ')
                if curr_passwd == passwd:
                    new_passwd = getpass.getpass(prompt='Enter new password: ')
                    #Sending new login credentials for curr user
                    s.sendto(username + '<>' + new_passwd, (host,port))
                    print 'Sent'

                    #print 'Waiting for response..'
                    #receive a response from server
                    #done = s.recv(7)

                    for tempSocket in readable:
                        done = tempSocket.recv(1024)
                    #print 'this is reply: ' + done
                    if done == 'done':
                        print 'Password changed successfully'
                        passwd = new_passwd
                else:
                    print 'Incorrect password. Please try again'
            if message == str(3):
                message = raw_input("Choose an option (type the number): \n 1. Private messages \n 2. Broadcast messages \n 3. Group messages \n")
                try :
                    '''
                    Part-2:TODO: Send option to server
                    '''
                    s.sendto(message, (host,port)) # Send option to server
                    if message == str(1):
                        pmsg = raw_input("Enter your private message\n")
                        try :
                            '''
                            Part-2:TODO: Send private message
                            '''
                            print 'Sending message ... '
                            s.sendto(pmsg, (host,port))
                            
                        except socket.error:
                            print 'Private Message Send failed'
                            sys.exit()
                        rcv_id = raw_input("Enter the recevier ID:\n")
                        try :
                            '''
                            Part-2:TODO: Send private message
                            '''
                            print 'Sending ID...'
                            s.sendto(rcv_id,(host,port))
                            break
                        except socket.error:
                            print 'rcv_id Send failed'
                            sys.exit()
                    if message == str(2):
                        bmsg = raw_input("Enter your broadcast message\n")
                        try :
                            '''
                            Part-2:TODO: Send broadcast message
                            '''
                            break
                        except socket.error:
                            print 'Broadcast Message Send failed'
                            sys.exit()
                    if message == str(3):
                        gmsg = raw_input("Enter your group message\n")
                        try :
                            '''
                            Part-2:TODO: Send group message
                            '''
                        except socket.error:
                            print 'Group Message Send failed'
                            sys.exit()
                        g_id = raw_input("Enter the Group ID:\n")
                        try :
                            '''
                            Part-2:TODO: Send group message
                            '''
                            break
                        except socket.error:
                            print 'g_id Send failed'
                            sys.exit()
                except socket.error:
                    print 'Message Send failed'
                    sys.exit()
            if message == str(4):
                #Group configuration
                option = raw_input("Do you want to: 1. Join Group 2. Quit Group: \n")
                if option == str(1):
                    group = raw_input("Enter the Group you want to join: ")
                    try :
                        '''
                        Part-2:TODO: Join a particular group
                        '''
                    except socket.error:
                        print 'group info sent failed'
                        sys.exit()
                elif option == str(2):
                    group = raw_input("Enter the Group you want to quit: ")
                    try :
                        '''
                        Part-2:TODO: Quit a particular group
                        '''
                    except socket.error:
                        print 'group info sent failed'
                        sys.exit()
                else:
                    print 'Option not valid'
            if message == str(5):
                #offline message
                while not os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
                    pass
                option = raw_input("Do you want to: 1. View all offline messages; 2. View only from a particular Group\n")
                if option == str(1):
                    try :
                        '''
                        Part-2:TODO: View all offline messages
                        '''
                    except socket.error:
                        print 'msg Send failed'
                        sys.exit()
                elif option == str(2):
                    group = raw_input("Enter the group you want to view the messages from: ")
                    try :
                        '''
                        Part-2:TODO: View only from a particular group
                        '''
                    except socket.error:
                        print 'group Send failed'
                        sys.exit()
                else:
                    print 'Option not valid'
            
                        
        except socket.error:
            print 'Send failed'
            sys.exit()
else:
    print 'Invalid username or password'

s.close()
