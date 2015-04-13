import urllib2  # the lib that handles the url stuff
#import split
    

data = urllib2.urlopen('http://engr.uconn.edu/~song/classes/cn/db').read() # it's a file like object and works just like a file
data = data.split('\n')
for line in data: # files are iterable
    print line

for line in data:
    print line.find('1234')    

