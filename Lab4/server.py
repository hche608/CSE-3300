import socket
import random
import struct
import urllib2  # the lib that handles the url stuff
import split
    
def get_db():
    data = urllib2.urlopen('http://engr.uconn.edu/~song/classes/cn/db') # it's a file like object and works just like a file
    data = data.split('\n')
    for line in data: # files are iterable
        print line
    return data        
# get sum of two integer
# 32 bits integer
def get_sum(i32):
    result = get_checksum((i32 >> 16), (i32 & 0x0000ffff))
    return result
# 16 bits integer
def get_sum(i16_1, i16_2):
    result = i16_1 + i16_2
    if result > 0x0000ffff:
        result = (result & 0x0000ffff) + 1
        print 'overflow'
    return result

db = get_db()

UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

timeout = 5.0

debug_checksum = 1

# package generator
if debug_checksum == 1:
    print bin(0x0000ffff)
head = 3300
lab_and_version_number = 1031
client_cookie = random.randint(5000, pow(2, 32))
ssn_request = random.randint(100000000, 999999999)


# start to calculate checksum
temp_sum = get_sum(head, lab_and_version_number)

if debug_checksum == 1:
    print 'h1.1: ' + bin(head)
    print 'h1.2: ' + bin(lab_and_version_number)    
    print 'H1  : ' + bin(temp_sum)
        
# second line    
temp = client_cookie >> 16
temp_sum = get_sum(temp_sum, temp)

    
if debug_checksum == 1:
    print 'h2.1: ' + bin(temp)  
    print 'H2  : ' + bin(temp_sum)

temp = client_cookie & 0x0000ffff
temp_sum = get_sum(temp_sum, temp)

if debug_checksum == 1:
    print 'h2.2: ' + bin(temp)  
    print 'H2  : ' + bin(temp_sum)

# third line
temp = ssn_request >> 16
temp_sum = get_sum(temp_sum, temp)

if debug_checksum == 1:
    print 'h3.1: ' + bin(temp)  
    print 'H3  : ' + bin(temp_sum)

temp = ssn_request & 0x0000ffff
temp_sum = get_sum(temp_sum, temp)

if debug_checksum == 1:
    print 'h3.2: ' + bin(temp)  
    print 'H3  : ' + bin(temp_sum)


# calculate checksum
checksum = ~temp_sum & 0x0000ffff

print 'checksum: ' + bin(checksum)

#
other = 0
pack = struct.pack('!2H2I2H', head, lab_and_version_number, client_cookie, ssn_request, checksum, other)

#print str(pack)

print struct.unpack('!2H2I2H', pack)
UDPSock.bind(('0.0.0.0', 0))

max_transmission = 5
while max_transmission > 0:
    UDPSock.sendto(pack, ('137.99.11.9', 3300))
    try:
        UDPSock.settimeout(timeout)
        print 'timeout, retransmission number ' + str(max_transmission)
        data, addr = UDPSock.recvfrom(30) # buffer size is 1024 bytes
        print "received message:", data
    except:
        pass
    max_transmission -= 1

