# sender.py - The sender in the reliable data transfer protocol
import packet
import socket
import sys
import thread
import time
import packet

from packet import make
from packet import extract

from timer import Timer


##TODO: Initialize the following variables
RECEIVER_ADDR = ('localhost',8080)
SENDER_ADDR = ('', 8080)
SLEEP_INTERVAL = 1
TIMEOUT_INTERVAL = 10
WINDOW_SIZE = 4

# base should increment to the next packet (within the same window) once an ack is received

# Shared resources across threads
base = 0
mutex = thread.allocate_lock()
send_timer = Timer(TIMEOUT_INTERVAL)

# Sets the window size
def set_window_size(num_packets):
    global base
    return min(WINDOW_SIZE, num_packets - base)
# Send thread
def send(sock):
    global mutex
    global base
    global send_timer

    ## TODO: Add all the packets and corresponding seq_num to packets
    packets = ['Message 1','Message 2','Message 3','Message 4','Message 5','Message 6','Message 7','Message 8','Message 9','Message 10','Message 11','Message 12']
    num_packets = len(packets)
    seq_num = 0
    

    ##TODO: Initialize window_size, next_to_send and base values
    window_size = set_window_size(num_packets)
    next_to_send = 0
    base = 0

    # Start the receiver thread
    thread.start_new_thread(receive, (sock,))

    while base < num_packets:
        mutex.acquire()
        # Send all the packets in the window
        while (next_to_send < base + window_size):
            # TODO: Send the packet and increase next_to_send counter
            print('Sending packet:', packets[next_to_send], seq_num)
            send_packet = make(seq_num, packets[next_to_send])
            
            sock.sendto(send_packet, (SENDER_ADDR))
            seq_num += 1
            next_to_send += 1
        # Start the timer
        if not send_timer.running():
            print('Starting timer')
            send_timer.start()

        # Wait until a timer goes off or we get an ACK
        while send_timer.running() and not send_timer.timeout():
            mutex.release()
            print('Sleeping')
            time.sleep(SLEEP_INTERVAL)
            mutex.acquire()

        if send_timer.timeout():
            # Looks like we timed out
            print('Timeout')
            send_timer.stop();
            ## TODO: Set appropriate value of next_to_send
            next_to_send = packets.pop(0) #change to a prev_next variable
        else:
            print('Shifting window')
            ## TODO:  Set the correct window_size
            window_size = set_window_size(num_packets)
            #base += 1
        mutex.release()
        #seq_num += 1

    # TODO: Send empty packet as an indicator to close the connection
    sock.sendto('', (RECEIVER_ADDR,SENDER_ADDR))
    
    #receive(sock)
    
    
#isAck function
def isACK(in_seq_num, base):
    if(in_seq_num != base):
        return False
        
    return True


# Receive thread
def receive(sock):
    global mutex
    global base
    global send_timer

    while True:
        # TODO: Reveive packet and extract data and ack
        d = sock.recvfrom(1024)
        data = d[0]
        print('Received data... Processing data')
        
        
        #idea: extract the ACK value from the received msg
        in_seq_num, msg = extract(data)
        
        #if not isACK(in_seq_num, base):
            #print('No ACK')
            #return False
        
        ack = in_seq_num
        
        # If we get an ACK for the first in-flight packet
        print('Got ACK', ack)
        print('Got reply: ' + msg)
        ack = int(ack)
        if (ack >= base):
            mutex.acquire()
            ## TODO: Set the correct value of base
            base += 1
            print('Base updated', base)
            send_timer.stop()
            mutex.release()

# Main function
if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind(SENDER_ADDR)

    send(sock)
    #receive(sock)
    sock.close()
