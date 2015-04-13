__author__ = 'hche608'
import random
import Cookie
import struct
import base64
import binascii


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


