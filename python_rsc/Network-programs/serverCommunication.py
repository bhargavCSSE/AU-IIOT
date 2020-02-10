import socket
import os

SERVER_PORT = 5000
SERVER_IP = '127.0.0.1'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen(3)
    print("Server listening....")
    conn, addr = s.accept()
    with conn:
        print("Connected to ", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            with open('received_file.txt', 'wb') as f:
                f.write(data)
                f.close
                print('Got file')
                s.close()
                print('connection closed')
