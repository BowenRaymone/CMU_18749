import socket
import sys
import argparse

YELLOW =    "\u001b[33m" # Server color
MAGENTA =   "\u001b[35m" # Client color
RESET =     "\u001b[0m"

def get_args():
    parser = argparse.ArgumentParser()

    # IP, PORT, Clientname, messageId
    parser.add_argument('-ip', '--ip', help="Server IP Address", default='localhost')
    parser.add_argument('-p', '--port', help="Server Port", type=int, default=5000)
    parser.add_argument('-c', '--clientname', help="Client name", required=True)
    parser.add_argument('-m', '--messageid', help="Message id", required=True)
    
    # Parse the arguments
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # Extract Arguments from the 
    args = get_args()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print (MAGENTA + 'connecting to {}'.format(server_address) + RESET)
    sock.connect(server_address)

    try:

        # Send data
        message = "<{},{}>".format(args.clientname,args.messageid)
        print(MAGENTA + 'sending ', message + RESET)
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        while amount_received < 20:
            data = sock.recv(16)
            amount_received += len(data)
            print (MAGENTA + 'received ', data.decode() + RESET)
            
    finally:
        print (MAGENTA + 'closing socket' + RESET)
        sock.close()
