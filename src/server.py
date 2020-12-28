import socket
import sys
import re
import argparse
import multiprocessing
import threading

YELLOW =    "\u001b[33m" # Server color
RESET =     "\u001b[0m"

# Server port port + 0: thread for client
# Server port port + 1: thread for lfd

class Server:
    def __init__(self, port=10000):
        self.port = port
        self.thread_running = True
        # Internal state variable
        self.state_var = 0

        # instantiate threads to handle various 
        threads = []

        try:
            threads.append(threading.Thread(target=self.handle_client, args=()))
            threads.append(threading.Thread(target=self.handle_lfd, args=()))

            for thread in threads:
                thread.start()

            while self.thread_running:
                continue
        except KeyboardInterrupt:
            server.thread_running = False
            sys.exit()
    
    def handle_client(self):
        print (YELLOW + 'start client thread' + RESET)
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', self.port)
        print (YELLOW + 'starting client on %s port %s' % server_address + RESET)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while self.thread_running:
            # Wait for a connection
            print (YELLOW + 'waiting for a connection' + RESET)
            connection, client_address = sock.accept()
            try:
                print(YELLOW + 'connection from {}'.format(client_address) + RESET)
                self.state_var += 1

                # Receive the data in small chunks and retransmit it
                client_name = ''
                message_id = -1
                while True:
                    data = connection.recv(16)
                    if data:
                        # read client name and message id from data with format "<c1,101>"
                        m = re.findall('<(?P<_0>.+)\,(\d+)>', data.decode())
                        client_name = m[0][0]
                        message_id = m[0][1]
                        response = "{}: {}. state_var = {}".format(client_name,message_id,self.state_var)
                        print(YELLOW + response + RESET)
                        connection.sendall(response.encode())
                    else:
                        #print('no more data from', client_address)
                        break
                
            finally:
                # Clean up the connection
                connection.close()
    
    def handle_lfd(self):
        print (YELLOW + 'start lfd thread' + RESET)
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', self.port+1)
        print (YELLOW + 'starting lfd on %s port %s' % server_address + RESET)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(5)

        while self.thread_running:
            # Wait for a connection
            print (YELLOW + 'lfd thread waiting for a connection' + RESET)
            connection, client_address = sock.accept()
            try:
                print(YELLOW + 'lfd connection from {}'.format(client_address) + RESET)

                while self.thread_running:
                    data = connection.recv(16).decode()
                    if data and data == 'alive':
                        connection.sendall(data.encode())
                    else:
                        break
            finally:
                connection.close()


def get_args():
    parser = argparse.ArgumentParser()

    # PORT
    parser.add_argument('-p', '--port', help="Server Port", type=int, default=10000)
    
    # Parse the arguments
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # Extract Arguments from the 
    args = get_args()

    server = Server(port=args.port)

    