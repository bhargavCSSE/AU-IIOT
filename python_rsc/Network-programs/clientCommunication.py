import socket
import os
from pathlib import Path

port = 5000
IP = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, port))

filename = Path("file.txt")
f = open(filename, "rb")
l = f.read(1024)
s.send(l)
print('Sent file',filename)
f.close()
s.close()
