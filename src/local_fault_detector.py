import socket
import sys
import re
import argparse
import time
from datetime import datetime

CYAN =      "\u001b[36m" # LFD color
RESET =     "\u001b[0m"

heartbeat_message = "alive"
alive_message = "Server on port {} is alive."
dead_message = "Server on port {} is dead."

class LocalFaultDetector:
    def __init__(self, lfd_port=10100, server_port=10001, hb_interval=1):
        self.lfd_port = lfd_port
        self.server_port = server_port
        self.hb_interval = hb_interval

        print (CYAN + 'LFD at port {}'.format(self.lfd_port) + RESET)
        print (CYAN + 'LFD connects to server port {}'.format(self.server_port) + RESET)
        print (CYAN + 'LFD hb_interval {}'.format(self.hb_interval) + RESET)

        while True:
            time.sleep(hb_interval)
            receive_message = ''

            try:
                # Create a TCP/IP socket to send heartbeat message
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect the socket to the port where the server is listening
                server_address = ('localhost', server_port)
                sock.connect(server_address)

                # Send heartbeat_message
                print(CYAN + 'sending ', heartbeat_message + RESET)
                sock.sendall(heartbeat_message.encode())

                # Look for the response
                amount_received = 0
                while amount_received < 5:
                    receive_message = sock.recv(16).decode()
                    amount_received += len(receive_message)
                    print (CYAN + 'received ', receive_message + RESET)
            except:
                receive_message = ''
            finally:
                print (CYAN + 'closing socket' + RESET)
                sock.close()

            current_timestamp = str(datetime.now())
            if receive_message == heartbeat_message:
                print(CYAN + current_timestamp + ' ' + alive_message.format(server_port) + RESET)
            else:
                print(CYAN + current_timestamp + ' ' + dead_message.format(server_port) + RESET)
            
            

if __name__ == '__main__':
    lfd = LocalFaultDetector()
