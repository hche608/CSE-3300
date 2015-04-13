#import socket
import urllib2


#host = socket.gethostbyname("http://jsonip.com/")
#port = 3300
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#sock.connect((host, port))


print urllib2.urlopen("http://jsonip.com/").read()





#print data

#sock.close()

