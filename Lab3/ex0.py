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
local_port = random.randint(0, 9000)

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

# generate msg
msg = 'ex0 ' + str(host_IP) + '-' + str(host_port) + ' ' + local_IP + '-' + str(local_port) + ' ' + str(random_port) + ' ' + name + '\n'
#print 'msg will be sent: ' + msg

# send msg
sock.send(msg)

data = sock.recv(rec_buffer)
# if received ack then keep going, else print an error
if data.find("OK") != -1:
    print data

    # read server numbers from received msg
    sqNum = data[data.index('OK ', 0, len(data)) + 3:data.index('OK ', 0, len(data)) + 3 + len(str(random_port))]
    num = data[data.index('HEN ', 0, len(data)) + 4:]

    msg = 'ex0 ' + str(random_port + 2) + ' ' + str(int(num) + 1) + '\n'
    print msg
    sock.send(msg)
    data = sock.recv(rec_buffer)

    # if received ack then keep going, else print an error
    if data.find("OK") != -1:
        print data
    else:
        print data + 'received an error from 2nd send!'
else:
    print data + 'received an error from 1st send!'

# close connection
sock.close()
