import socket
import Cookie

BUFFER_SIZE = 1024
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("tao.ite.uconn.edu",80))

MESSAGE = "Hello, World!"

print Cookie.SimpleCookie()

