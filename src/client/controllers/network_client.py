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
        self.connect()

    def connect(self):
        "Connects to server"
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.host, self.port))

            handler = threading.Thread(target=self.handleResponse,)
            handler.start()
        except:
            print("There was an error connecting")

    def sendRequest(self, request):
        print("request going to server")
        request_dump = json.dumps(request)
        
        self.s.sendall(request_dump.encode('utf-8'))



    def handleResponse(self):
        while True:
            
            try:
                data = self.s.recv(1024).decode('utf-8')

                if not data:
                    break
                
                response = data
                try:
                    response = json.loads(data)
                    print(f"Received response: {response}")
                except:
                    logging.error("Error loading JSON", exc_info=True)

                print(f"{response}")
                try:
                    "Incase there is not message received"
                    if response['type'] == "uniqueID_response":
                        print(response['data'][0]['uniqueID'])
                except:
                    print("No response received yet.")
            except:
                logging.error("There was an error receiving the message", exc_info=True)
                print("Error receiving data")
                break

    def testPrint(self):
        print("Object istantiated")
