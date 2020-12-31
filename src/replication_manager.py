import socket
import sys
import re
import argparse
import server
import multiprocessing
import local_fault_detector
import global_fault_detector
import threading
import json

BLACK =     "\u001b[30m"
RED =       "\u001b[31m" # GFD color
GREEN =     "\u001b[32m" # RM color
YELLOW =    "\u001b[33m" # Server color
BLUE =      "\u001b[34m" # Not use.
MAGENTA =   "\u001b[35m" # Client color
CYAN =      "\u001b[36m" # LFD color
RESET =     "\u001b[0m"

def instantiate_server(id, port):
    server.Server(id=id, port=port)

def instantiate_lfd(id, lfd_port, server_port, hb_interval):
    local_fault_detector.LocalFaultDetector(id=id, lfd_port=lfd_port, server_port=server_port, hb_interval=hb_interval)

def instantiate_gfd(hb_interval):
    global_fault_detector.GlobalFaultDetector(hb_interval=hb_interval)

# RM is listening at 15000 from GFD for membership report
class ReplicationManager:

    def __init__(self, mode='active', rm_port=15000, gfd_port=15001, gfd_hb_interval=1):
        self.mode = mode
        self.rm_port = rm_port
        self.gfd_port = gfd_port
        self.gfd_isAlive = False
        self.gfd_hb_interval = gfd_hb_interval
        self.server_default_port = 10000
        self.thread_running = True
        self.active_replicas = [1,2,3]

        for i in range(3):
            server_port = self.server_default_port+i*10
            # instantiate a server at one process
            p = multiprocessing.Process(target=instantiate_server, args=(i, server_port, ))
            p.start()
            # instantiate a LFD at another process
            p = multiprocessing.Process(target=instantiate_lfd, args=(i, server_port+100, server_port+1, self.gfd_hb_interval, ))
            p.start()
        
        # instantiate GFD at another process
        p = multiprocessing.Process(target=instantiate_gfd, args=(self.gfd_hb_interval,))
        p.start()

        # instantiate threads to handle various tasks
        threads = []
        try:
            threads.append(threading.Thread(target=self.handle_gfd_membership, args=()))

            for thread in threads:
                thread.start()

            while self.thread_running:
                continue
        except KeyboardInterrupt:
            server.thread_running = False
            sys.exit()

        print(GREEN + "Replication Manager process started" + RESET)
    
    def handle_gfd_membership(self):
        print (GREEN + 'Start gfd membership thread' + RESET)
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', self.rm_port)
        print (GREEN + 'starting on port {}'.format(self.rm_port) + RESET)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while self.thread_running:
            # Wait for a connection
            connection, client_address = sock.accept()
            try:
                print(GREEN + 'connection from {}'.format(client_address) + RESET)

                while self.thread_running:
                    data = connection.recv(24).decode()
                    if data:
                        # read membership list from data with format "[1,2,3,]"
                        self.active_replicas = json.loads(data)
                        print(GREEN + "active_replicas: " , json.dumps(self.active_replicas) + RESET)
                    else:
                        break
                
            finally:
                # Clean up the connection
                connection.close()

def get_args():
    parser = argparse.ArgumentParser()

    # Heartbeat Frequency
    parser.add_argument('-hbf', '--hb_freq', help="Heartbeat Frequency", type=int, default=1)
    
    # Parse the arguments
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # Extract Arguments 
    args = get_args()

    rm = ReplicationManager(gfd_hb_interval=args.hb_freq)
