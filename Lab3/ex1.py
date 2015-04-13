import socket
import random
import urllib
import re


# get external IP address
def get_ip():
    group = re.compile(u'(?P<ip>\d+\.\d+\.\d+\.\d+)').search(urllib.URLopener().open('http://jsonip.com/').read()).groupdict()
    return group['ip']


# initial everything
local_IP = get_ip()

host_IP = socket.gethostbyname("tao.ite.uconn.edu")
host_port = 3300

# TCP via ipv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
name = 'H.CHEN'
# Generate a random server number
random_port = random.randint(0, 9000)
rec_buffer = 1480

# setup connection
sock.connect((host_IP, host_port))

# Second socket
psock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a random port
psock.bind(('', 0))

# Listen for incoming connections
psock.listen(5)

# local port
local_port = psock.getsockname()[1]

# generate msg
msg = 'ex1 ' + str(host_IP) + '-' + str(host_port) + ' ' + local_IP + '-' + str(local_port) + ' ' + str(random_port) + ' ' + name + '\n'

# send msg
sock.send(msg)

data = sock.recv(rec_buffer)
num = int(data[data.index('HEN ', 0, len(data)) + 4:]) + 1  # get servernum + 1
print data
if data.find("OK") != -1:
    while True:
        # Wait for a connection
        client, client_address = psock.accept()
        data = client.recv(rec_buffer)
        print data

        if data:
            msg = str(num) + ' ' + str(int(data[data.index('calling ', 10, len(data))+8:])+1) + '\n'

            client.send(msg)
            data = sock.recv(rec_buffer)
            print data
            if data.find("OK") != -1:
                client.close()
            else:
                print 'error from 3rd step'
        else:
            print 'error from 2nd step'
        break
else:
    print 'error from 1st step '

# close connection
sock.close()
