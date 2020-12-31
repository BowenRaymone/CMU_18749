import socket
import sys
import re
import argparse
import time
from datetime import datetime
import threading
from collections import OrderedDict 
import json

RED =       "\u001b[31m" # GFD color
RESET =     "\u001b[0m"

heartbeat_message = "gfd_alive"
alive_message = "LFD on port {} is alive."
dead_message = "LFD on port {} is dead."

# GFD heartbeat port 10200: thread for heartbeat
# GFD membership port 10201: thread for membership change report from lfd 
# GFD membership report port 10202: thread for reporting membership change to RM

class GlobalFaultDetector:
    def __init__(self, gfd_port=10200, lfd_port=10101, hb_interval=1):
        self.gfd_port = gfd_port
        self.lfd_port = lfd_port
        self.hb_interval = hb_interval
        self.thread_running = True
        self.views = OrderedDict()
        self.rm_port = 15000

        print (RED + 'GFD at port {} and hb_interval {}'.format(self.gfd_port, self.hb_interval) + RESET)

        # instantiate threads to handle various tasks
        threads = []

        try:
            threads.append(threading.Thread(target=self.handle_lfd_heartbeat, args=()))
            threads.append(threading.Thread(target=self.handle_rm_membership, args=()))

            for thread in threads:
                thread.start()

            while self.thread_running:
                continue
        except KeyboardInterrupt:
            server.thread_running = False
            sys.exit()

    def handle_lfd_heartbeat(self):
        while self.thread_running:
            time.sleep(self.hb_interval)
            receive_message = ''
            current_replicas = []

            for i in range(3):
                try:
                    # Create a TCP/IP socket to send heartbeat message
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Connect the socket to the port where the server is listening
                    lfd_port_i = self.lfd_port+10 * i;
                    server_address = ('localhost', lfd_port_i)
                    print (RED + 'connecting to {}'.format(server_address) + RESET)
                    sock.connect(server_address)

                    # Send heartbeat_message
                    print(RED + 'sending ', heartbeat_message + RESET)
                    sock.sendall(heartbeat_message.encode())

                    # Look for the response
                    receive_message = sock.recv(24).decode()
                    print (RED + 'received ', receive_message + RESET)
                except:
                    receive_message = ''
                finally:
                    sock.close()

                current_timestamp = str(datetime.now())
                if receive_message == heartbeat_message:
                    print(RED + current_timestamp + ' ' + alive_message.format(lfd_port_i) + RESET)
                    current_replicas.append(i)
                else:
                    print(RED + current_timestamp + ' ' + dead_message.format(lfd_port_i) + RESET)
            
            current_timestamp = str(datetime.now())
            self.views[current_timestamp] = current_replicas
            print(RED + 'views: ', str(self.views) + RESET)

    def handle_rm_membership(self):
        print (RED + 'handle_rm_membership ' + RESET)

        while self.thread_running:
            time.sleep(15) # hard-code 15 secs as rm submission time

            try:
                # Create a TCP/IP socket to send heartbeat message
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect the socket to the port where the RM is listening
                server_address = ('localhost', self.rm_port)
                print (RED + 'connecting to {}'.format(server_address) + RESET)
                sock.connect(server_address)

                # Send heartbeat_message: [] current active replica list
                latest_timestamp = next(reversed(self.views))
                message = json.dumps(self.views[latest_timestamp])
                print(RED + 'sending membership list', message + RESET)
                sock.sendall(message.encode())

            finally:
                sock.close()
                

if __name__ == '__main__':
    gfd = GlobalFaultDetector()
