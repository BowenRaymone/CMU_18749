import socket
import sys
import re
import argparse
import time
from datetime import datetime
import threading

CYAN =      "\u001b[36m" # LFD color
RESET =     "\u001b[0m"

heartbeat_message = "alive"
gfd_heartbeat_message = "gfd_alive"
alive_message = "[{}]: Server on port {} is alive."
dead_message = "[{}]: Server on port {} is dead."

# lfd port + 0: thread for server heartbeat
# lfd port + 1: thread for gfd heartbeat

class LocalFaultDetector:
    def __init__(self, id, lfd_port=10100, server_port=10001, hb_interval=1):
        self.id = id
        self.lfd_port = lfd_port
        self.server_port = server_port
        self.hb_interval = hb_interval
        self.thread_running = True

        print (CYAN + 'LFD {} at port {}'.format(self.id, self.lfd_port) + RESET)
        print (CYAN + 'LFD {} connects to server port {}'.format(self.id, self.server_port) + RESET)
        print (CYAN + 'LFD {} hb_interval {}'.format(self.id, self.hb_interval) + RESET)

        # instantiate threads to handle various tasks
        threads = []

        try:
            threads.append(threading.Thread(target=self.handle_server_heartbeat, args=()))
            threads.append(threading.Thread(target=self.handle_gfd_heartbeat, args=()))

            for thread in threads:
                thread.start()

            while self.thread_running:
                continue
        except KeyboardInterrupt:
            server.thread_running = False
            sys.exit()

    def handle_server_heartbeat(self):
        while self.thread_running:
            time.sleep(self.hb_interval)
            receive_message = ''

            try:
                # Create a TCP/IP socket to send heartbeat message
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect the socket to the port where the server is listening
                server_address = ('localhost', self.server_port)
                sock.connect(server_address)

                # Send heartbeat_message
                sock.sendall(heartbeat_message.encode())

                # Look for the response
                receive_message = sock.recv(16).decode()
                print (CYAN + 'received ', receive_message + RESET)  
            except:
                receive_message = ''
            finally:
                sock.close()

            current_timestamp = str(datetime.now())
            if receive_message == heartbeat_message:
                print(CYAN + current_timestamp + ' ' + alive_message.format(self.id, self.server_port) + RESET)
            else:
                print(CYAN + current_timestamp + ' ' + dead_message.format(self.id, self.server_port) + RESET)

    def handle_gfd_heartbeat(self):
        print (CYAN + '[{}] start gfd heartbeat thread'.format(self.id) + RESET)
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', self.lfd_port+1)
        print (CYAN + '[{}] starting gfd on {} port {}'.format(self.id, 'localhost', self.lfd_port+1) + RESET)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while self.thread_running:
            # Wait for a connection
            connection, client_address = sock.accept()
            try:
                print(CYAN + '[{}] gfd connection from {}'.format(self.id, client_address) + RESET)

                while self.thread_running:
                    data = connection.recv(16).decode()
                    if data and data == gfd_heartbeat_message:
                        connection.sendall(data.encode())
                    else:
                        break
            finally:
                connection.close()
            

if __name__ == '__main__':
    lfd = LocalFaultDetector()
