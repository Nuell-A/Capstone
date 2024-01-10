import socket
import threading
import sys
import time

sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")

import config


'''This file will handle the hosting of the server on the itnernet.'''

def socketStart():
    print("Starting socket...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((config.socket_host, config.socket_port))
        s.listen()
        print("Awaiting client connection")
        # Once accept is called it blocks script execution, hence while threading is needed.
        conn, addr = s.accept() # conn = new socket object, addr = client address 

        print(f"Client connected: {addr}")
        while conn:
            while True:
                message = conn.recv(1024)
                if not message:
                    break
                conn.sendall(message)

def testFunction():
    for x in range(1, 15):
        print(x)
        time.sleep(2)

socket_listen = threading.Thread(target=socketStart)
socket_listen.start()

test = threading.Thread(target=testFunction)
test.start()
