import socket
import sys

sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")

import config

# Using with statment means that we do not have to close the socket,
# . it closes on its own.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Initiate connection with server host/port combo.
    s.connect((config.socket_host, config.socket_port))

    while True:
        message = input("Type a message:")
        if not message:
            break
        s.sendall(message.encode("utf-8"))
        receive = s.recv(1024)
        print(receive)

