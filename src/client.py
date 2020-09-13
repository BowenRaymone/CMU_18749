import socket
import sys
import argparse

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
    print ('connecting to ', server_address)
    sock.connect(server_address)

    try:

        # Send data
        message = "<{},{}>".format(args.clientname,args.messageid)
        print('sending ',message)
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        while amount_received < 20:
            data = sock.recv(16)
            amount_received += len(data)
            print ('received ', data.decode())
            
    finally:
        print ('closing socket')
        sock.close()
