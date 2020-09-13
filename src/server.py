import socket
import sys
import re

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Internal state variable
state_var = 0

while True:
    # Wait for a connection
    print ( 'waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        state_var += 1

        # Receive the data in small chunks and retransmit it
        client_name = ''
        message_id = -1
        while True:
            data = connection.recv(16)
            #print ('received "%s"' % data)
            if data:
                # read client name and message id from data with format "<c1,101>"
                m = re.findall('<(?P<_0>.+)\,(\d+)>', data.decode())
                client_name = m[0][0]
                message_id = m[0][1]
                response = "{}: {}. state_var = {}".format(client_name,message_id,state_var)
                print (response)
                connection.sendall(response.encode())
            else:
                #print('no more data from', client_address)
                break
        
    finally:
        # Clean up the connection
        connection.close()