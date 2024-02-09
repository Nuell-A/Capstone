import socket
import json
import threading
import logging

import sys
sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")
sys.path.insert(2, "C:\\Users\\alcal\\Documents\\Projects\\Capstone\\Capstone\\src") # Windows
import config

class NetworkClient:

    def __init__(self):
        logging.basicConfig(filename="network_client.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
        self.host = config.socket_host
        self.port = config.socket_port
        self.s = None
        self.callback_response = None
        self.connect()

    def connect(self):
        "Connects to server"
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(("172.30.21.2", self.port))
            handler = threading.Thread(target=self.handleResponse,)
            handler.start()
            print("Successfully connected to server... ready to handle send/receives.")
        except:
            print("There was an error connecting")

    def sendRequest(self, request):
        request_dump = json.dumps(request)
        self.s.sendall(request_dump.encode('utf-8'))
        print(f"REQUEST sent. {request}\n")

    def setCallbackResponse(self, callback):
          self.callback_response = callback
          
    def processResponse(self, response):
        try:
            if self.callback_response:
                self.callback_response(response)
                print("")
        except:
              print("There was an error processing the response.")
              logging.error("PROCESSING RESPONSE ERROR: ", exc_info=True)

    def handleResponse(self):
        while True:
            try:
                data = self.s.recv(1024).decode('utf-8')
                
                if not data:
                    break

                response  = json.loads(data)
                print("RESPONSE received.")
                print(response)
                self.processResponse(response)
            except:
                print("There was an error receiving data.")
                logging.error("RECEVING ERROR: ", exc_info=True)
                self.s.close()
                break