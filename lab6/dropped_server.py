# This server file will simulate what happens when a packet is dropped
# receiver.py - The receiver in the reliable data transer protocol
import packet
import socket
import sys

from packet import extract
from packet import make

from random import seed
from random import randint

RECEIVER_ADDR = ('localhost', 8080)

seed(1)

# Receive packets from the sender
def receive(sock):
    expected_num = 0
    while True:
        packet_fail_counter = randint(0,11)
        # TODO: Get the next packet from the sender
        d = sock.recvfrom(1024)
        pkt = d[0]
        addr = d[1]
        if not pkt or pkt == '':
            break
        seq_num, data = packet.extract(pkt)
        print('Got packet', seq_num)
        reply = 'OK...' + data
        
        if seq_num == packet_fail_counter:
            print ('Packet' , packet_fail_counter , ' has failed')
        
        # TODO: Make and send back an ACK for both conditions accordingly
        elif seq_num == expected_num:
            print('Data received:', data)
            send_pkt = make(expected_num, reply)
            sock.sendto(send_pkt, addr)
            expected_num += 1
        else:
            print('Sending ACK', expected_num - 1)
            send_pkt = make(expected_num - 1, reply)
            sock.sendto(send_pkt, addr)
            del pkt

# Main function
if __name__ == '__main__':
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    print 'Socket created'
    sock.bind(RECEIVER_ADDR)
    
    receive(sock)
    sock.close()

