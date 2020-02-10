import socket
import os
from pathlib import Path

port = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))

s.listen(3)
filename = Path("file.csv")
while(True):
    conn, addr = s.accept()
    data = conn.recv(1024)
    f = open(filename, "rb")
    l = f.read(1024)
    print(filename)
    while(l):
        conn.send(l)
        print('Sent file',repr(l))
        l = f.read(1024)
        f.close()
s.close()
