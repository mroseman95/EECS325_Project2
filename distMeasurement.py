#!/usr/bin/ python2.7

"""
EECS325 Project 2
Auth: Matthew Roseman | mrr77@case.edu

Code stolen from:
   "https://blogs.oracle.com/ksplice/entry/learning_by_doing_writing_your"
"""

import socket, sys, time
from struct import *

def main():

    targets = open('targets.txt', 'r')
    #  read every target from the file targets
    for dest_name in targets:
        #  remove the newline character
        dest_name = dest_name.rstrip()
        dest_addr = socket.gethostbyname(dest_name)

        udp = socket.getprotobyname('udp')
        icmp = socket.getprotobyname('icmp')
        ttl = 32
        port = 33434

        #  create the sending socket (udp packets)
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        #  set the ttl of the socket
        send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        #  create the receiving socket (icmp packets)
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

        recv_sock.bind(("", port))
        #  used later to calculate RTT
        time_sent = time.time()
        send_sock.sendto("", (dest_name, port))

        try:
            resp_data, resp_addr = recv_sock.recvfrom(512)
            #  used to calculate RTT
            time_recv = time.time()
            resp_addr = resp_addr[0]
        except socket.error:
            pass
        print (resp_addr)
        print (resp_data)
        print (''.join(format(ord(x), 'b') for x in resp_data))
        #  TODO: read the response datagram and get remaining ttl
        #  don't know why this section is the header and not the beginning  
        icmp_header = resp_data[20:28]
        type, code, checksum, p_id, sequence = unpack('bbHHh', icmp_header)
        print ("RTT: " + str((time_recv - time_sent) * 1000) + "msec")
        print ("ICMP type: " + str(type))
        print ("ICMP code: " + str(code))
        #  the data of the icmp
        icmp_data = resp_data[28:]
        print ("ICMP body length: " + str(len(icmp_data)))



if __name__ == '__main__':
    main()
