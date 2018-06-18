#!/usr/bin/env python3

import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5008
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)

while 1:
    data = conn.recv(BUFFER_SIZE)
    print ("received data:", data)

    if data:
        conn.send(data)
    # time.sleep(1)
    #

print ("close")
s.close()
conn.close()