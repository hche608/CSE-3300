import socket
import random
import struct
import urllib2  # the lib that handles the url stuff
import re


# get external IP address
def get_ip():
    host_ip_address = re.compile(u'(?P<ip>\d+\.\d+\.\d+\.\d+)').search(urllib2.urlopen('http://jsonip.com/').read()).groupdict()
    return host_ip_address['ip']


# get sum of two integer
# 16 bits unsigned integer
def get_sum(unsigned16_1, unsigned16_2):
    result = unsigned16_1 + unsigned16_2
    if result > 0x0000ffff:
        result = (result & 0x0000ffff) + 1
    return result


# calculate the checksum
def get_checksum(unsigned16_1, unsigned16_2, unsigned32_1, unsigned32_2, unsigned16_3):
    # start to calculate checksum
    temp_sum = get_sum(unsigned16_1, unsigned16_2)

    # second line
    temp = unsigned32_1 >> 16
    temp_sum = get_sum(temp_sum, temp)

    temp = unsigned32_1 & 0x0000ffff
    temp_sum = get_sum(temp_sum, temp)

    # third line
    temp = unsigned32_2 >> 16
    temp_sum = get_sum(temp_sum, temp)

    temp = unsigned32_2 & 0x0000ffff
    temp_sum = get_sum(temp_sum, temp)

    # forth line
    temp_sum = get_sum(temp_sum, unsigned16_3)
    # calculate checksum
    result = ~temp_sum & 0x0000ffff
    return result

# initial a UDP socket
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set timeout value
timeout = 5.0

# package generator
head = 3300
lab_and_version_number = 1031
client_cookie = random.randint(5000, pow(2, 32))
ssn_request = 111111111  # random.randint(100000000, 999999999)#
other = 0


# ask for user input
while 1:
    request_type = raw_input('Request type [0 or 1]: ')
    if request_type == '' or request_type == '0':
        break
    elif request_type == '1':
        head = 36068
        break


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
        except socket.gaierror:  # can throw an exception
            print 'Domain name is not correct.'

# get SUT port from user
host_port = 0
while 1:
    try:
        host_port = raw_input('Default SUT port is 3300, press Enter to continue or give a SUT port number: ')
        if host_port == '':
            host_port = 3300
            break
        elif 0 < int(host_port) < 65536:
            host_port = int(host_port)
            break
    except ValueError:
        pass

if head != 36068:
    # get input from user
    ssn = -1
    while 1:
        try:
            ssn = int(raw_input('Enter SSN [987654321]: '))
            if ssn == '':
                break
            elif 0 < int(ssn) < 1000000000:
                ssn_request = int(ssn)
                break
        except ValueError:
            pass

host_address = 0
if head == 36068:
    # SUT port is 3200
    other = 3200
    server_ip = get_ip()
    server_ip = server_ip.split('.')
    part_a, part_b, part_c, part_d = server_ip
    try:
        part_a = int(part_a) << 24
        part_b = int(part_b) << 16
        part_c = int(part_c) << 8
        part_d = int(part_d)
        host_address = part_a | part_b | part_c | part_d
    except ValueError:
        pass

if head == 36068:
    ssn_request = host_address
checksum = get_checksum(head, lab_and_version_number, client_cookie, ssn_request, other)
# define variables for further using
data = None
unpacked_msg = None
packed_msg = struct.pack('!2H2I2H', head, lab_and_version_number, client_cookie, ssn_request, checksum, other)

print struct.unpack('!2H2I2H', packed_msg)

max_transmission = 5
retransmission_counter = 1
while max_transmission > 0:
    UDPSock.sendto(packed_msg, (host_IP, host_port))  # 137.99.11.9, 127.0.0.1
    try:
        UDPSock.settimeout(timeout)

        data, client_address = UDPSock.recvfrom(20)  # buffer size is 1024 bytes
        if data:
            print "received message:", struct.unpack('!2H2I2H', data)
            unpacked_msg = struct.unpack('!2H2I2H', data)
            if unpacked_msg[4] == get_checksum(unpacked_msg[0], unpacked_msg[1], unpacked_msg[2], unpacked_msg[3], unpacked_msg[5]):
                break
            else:
                continue
    except socket.timeout:
        print 'timeout, retransmission ' + str(retransmission_counter)
        retransmission_counter += 1
        pass
    max_transmission -= 1

if unpacked_msg is not None:
    if unpacked_msg[5] & 0x8000 != 0:
        if unpacked_msg[5] == 32769:
            print 'Checksum Error'
        elif unpacked_msg[5] == 32770:
            print 'Syntax Error'
        elif unpacked_msg[5] == 32772:
            print 'Unknown SSN'
        elif unpacked_msg[5] == 32776:
            print 'Server Error'
        else:
            print 'Unknown Error'
    elif unpacked_msg[0] == 19684:
        print 'Post Office Box number: ' + str(unpacked_msg[5])
    elif unpacked_msg[0] == 52452:
        print 'Received a correct type1 msg.'
else:
    print 'No response from Server.'