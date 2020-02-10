import socket
import os

SERVER_PORT = 5000


s = socket.socket()
host = socket.gethostbyname("172.19.171.152")
s.connect((host, SERVER_PORT))

print("Server listening....")

with open('received_file', 'wb') as f:
    while True:
        data = s.recv(1024)
        f.write(data)
f.close
print('Got file')
s.close()
print('connection closed')
