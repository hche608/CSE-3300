import socket
import random
import struct

# initial everything

# get request_type from user
request_type = None
while 1:
    request_type = int(raw_input('Request type [0 or 1]: '))
    if request_type == 1 or request_type == 0:
        break
#print 'Request type is ' + str(request_type)

# get SUT IP from user
host_IP = None
while 1:
    host_IP = raw_input('Default SUT domain is "tao.ite.uconn.edu", press Enter to continue or give a SUT domain name: ')
    if host_IP == '':
        host_IP = socket.gethostbyname("tao.ite.uconn.edu")
        break
    else:
        try:
            host_IP = socket.gethostbyname(host_IP)
            break
        except socket.gaierror: #can throw an exception
            print 'Domain name is not correct.'
#print 'SUT IP is ' + str(host_IP)

# get SUT port from user

host_port = None
while 1:
    host_port = raw_input('Default SUT port is 3300, press Enter to continue or give a SUT port number: ')
    if host_port == '':
        host_port = 3300
    if 0 < int(host_port) < 65536:
        break
#print 'Host port is ' + str(host_port)

host = (host_IP, host_port)

# get input from user
ssn = -1
while 1:
    ssn = raw_input('Enter SSN [987654321]: ')
    if ssn == '':
        pass
    elif 0 < int(ssn) < 1000000000:
        break
#print 'SSN is ' + str(ssn)


# Create UDP socket via IPv4
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

timeout = 5.0

#socket.socket.settimeout(timeout)
# package generator

head = 3300
lab_and_version_number = 1031
client_cookie = random.randint(5000, pow(2, 32))
ssn_request = 1111111111
checksum = (client_cookie & ssn_request) & 0x0000ffff
if checksum > pow(2, 16):
    print checksum
    checksum &= 0x0000ffff + 1
print checksum
other = 0
pack = struct.pack('!2H2I2H', head, lab_and_version_number, client_cookie, ssn_request, checksum, other)

print struct.unpack('!2H2I2H', pack)


UDPSock.sendto(pack, host)

while True:
    data, addr = UDPSock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data