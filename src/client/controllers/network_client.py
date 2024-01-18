import socket
import json
import threading

import sys
sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")
sys.path.insert(2, "C:\\Users\\alcal\\Documents\\Projects\\Capstone\\Capstone\\src") # Windows
import config

class NetworkClient:

    def __init__(self):
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
                data = self.s.recv(2048)

                if not data:
                    break

                response = data.decode()
                response_object = json.loads(response)
                print(f"Received response: {response_object}")

                if response_object['type'] == "uniqueID_response":
                    print(response_object['data', 'uniqueID'])
            except:
                print("Error receiving data")
                break

    def testPrint(self):
        print("Object istantiated")
