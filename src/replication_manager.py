import socket
import sys
import re
import argparse
import server
import multiprocessing
import local_fault_detector

BLACK =     "\u001b[30m"
RED =       "\u001b[31m" 
GREEN =     "\u001b[32m" # RM color
YELLOW =    "\u001b[33m" # Server color
BLUE =      "\u001b[34m" # Not use.
MAGENTA =   "\u001b[35m" # Client color
CYAN =      "\u001b[36m" # LFD color
WHITE =     "\u001b[37m"
RESET =     "\u001b[0m"

def instantiate_server(port):
    server.Server(port=port)

def instantiate_lfd(lfd_port, server_port, hb_interval):
    local_fault_detector.LocalFaultDetector(lfd_port=lfd_port, server_port=server_port, hb_interval=hb_interval)

class ReplicationManager:

    def __init__(self, mode='active', rm_port=15000, gfd_port=15001, gfd_hb_interval=1):
        self.mode = mode
        self.rm_port = rm_port
        self.gfd_port = gfd_port
        self.gfd_isAlive = False
        self.gfd_hb_interval = gfd_hb_interval
        self.server_default_port = 10000

        for i in range(3):
            server_port = self.server_default_port+i*10
            # instantiate a server at one process
            p = multiprocessing.Process(target=instantiate_server, args=(server_port, ))
            p.start()
            # instantiate a LFD at another process
            p = multiprocessing.Process(target=instantiate_lfd, args=(server_port+100, server_port+1, self.gfd_hb_interval, ))
            p.start()
            
        print(GREEN + "Replication Manager process started" + RESET)


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
