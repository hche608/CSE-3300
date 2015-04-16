import socket
import struct
import urllib2  # the lib that handles the url stuff
import re


# get external IP address
def generate_msg(unsigned16_1, unsigned16_2, unsigned32_1, unsigned32_2, unsigned16_3):
    temp = get_checksum(unsigned16_1, unsigned16_2, unsigned32_1, unsigned32_2, unsigned16_3)
    result = struct.pack('!2H2I2H', unsigned16_1, unsigned16_2, unsigned32_1, unsigned32_2, temp, unsigned16_3)
    return result


def get_ip():
    group = re.compile(u'(?P<ip>\d+\.\d+\.\d+\.\d+)').search(urllib2.urlopen('http://jsonip.com/').read()).groupdict()
    return group['ip']


def get_db():
    db = urllib2.urlopen('http://engr.uconn.edu/~song/classes/cn/db').read()  # it's a file like object and works just like a file
    db = db.split('\n')
    return db


def get_ssn(value):
    result = 32772
    if value > 99999999:
        for line in ssn_db:
            if line.find(str(value)) != -1:  # Find Post Office Box number
                result = int(line[len(line) - 4:])
                print 'Requested SSN is found: %s' % result
                break
    if result == 32772:
        print 'Requested SSN is not found.'
    return result


# get sum of two integer
# 16 bits unsigned integer
def get_sum(unsigned16_1, unsigned16_2):
    result = unsigned16_1 + unsigned16_2
    if result > 0x0000ffff:
        result = (result & 0x0000ffff) + 1
    return result


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

ssn_db = get_db()

UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

head = 19684
lab_and_version_number = 1031
info_field = 0
host_port = 3200

UDPSock.bind(('', host_port))

# Checksum > Syntax Error > Unknown SSN > Server Error
print 'UDP server is listening port %s...' % host_port
while 1:
    data, client_address = UDPSock.recvfrom(20)  # buffer size is 20 bytes
    unpacked_msg = struct.unpack('!2H2I2H', data)
    msg_type = 1
    if unpacked_msg[0] == 3300:
        msg_type = 0
    print 'Type[%s] MSG Received From %s\nContent: %s' % (msg_type, client_address, unpacked_msg)
    checksum = get_checksum(unpacked_msg[0], unpacked_msg[1], unpacked_msg[2], unpacked_msg[3], unpacked_msg[5])
    if checksum != unpacked_msg[4]:  # check if there is an error in transmission
        print 'checksum is not match.'
        data = generate_msg(head, lab_and_version_number, unpacked_msg[2], unpacked_msg[3], 32769)
    else:
        print 'checksum is correct.'
        request_ssn = get_ssn(unpacked_msg[3])
        if unpacked_msg[0] != 3300 or unpacked_msg[1] != 1031:
            data = generate_msg(head, lab_and_version_number, unpacked_msg[2], unpacked_msg[3], 32770)
        elif request_ssn > 0:
            data = generate_msg(head, lab_and_version_number, unpacked_msg[2], unpacked_msg[3], request_ssn)
        else:
            data = generate_msg(head, lab_and_version_number, unpacked_msg[2], unpacked_msg[3], 32776)
    print 'MSG will be send: ', struct.unpack('!2H2I2H', data)
    UDPSock.sendto(data, client_address)
