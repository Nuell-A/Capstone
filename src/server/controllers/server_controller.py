import socket
import threading
import json
import logging

import sys
sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")
sys.path.insert(2, "C:\\Users\\alcal\\Documents\\Projects\\Capstone\\Capstone\\src") # Windows
import config
from server.database.game_management import GameManagement
from server.database.db_connection import Database




'''This file will handle the hosting of the server on the itnernet.'''
class ServerController:
    def __init__(self):
        logging.basicConfig(filename="server_controller.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
        self.db = None
        self.gm = None
        self.main()

    def sendResponse(self, conn, response):
        response_json = json.dumps(response)

        conn.sendall(response_json.encode('utf-8'))
        print("Sent RESPONSE.")
        
    def processRequest(self, request, conn):
        if request['type'] == "uniqueID":
            print("Creating unique ID....")

            response = self.gm.getUniqueID()    
            self.sendResponse(conn, response)

        elif request['type'] == "question_set":
            print("Getting question set...")

            response = self.gm.getQuestions(5)
            self.sendResponse(conn, response)

    def handleClient(self, conn, addr):
        try:
            print(f"Handling client: {addr}")
            while True:
                data = conn.recv(1024).decode('utf-8')
                
                if not data:
                    break
                print("REQUEST Recieved")
                request = json.loads(data)
                self.processRequest(request, conn)
        except:
            logging.error("Error sending message", exc_info=True)
            print("Closing connection.")
            return
        
        print("Client disconnected: " + str(addr))
    
    def checkJoinSession(self):
        '''Takes game ID from request and checks it against database (if it exists).
        Returns approve or denied (if not exists)'''
        return "Joined session"

    def main(self):
        self.db = Database()
        self.gm = GameManagement(self.db)
        print("Starting socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4 and TCP
        try:
            s.bind((config.socket_host, config.socket_port))
            s.listen()
            print("Socket binded successfully.")
            # Once accept is called it blocks script execution, hence while threading is needed.
        
        
        
            print("Ready to accept clients:")
            while True:
                conn, addr = s.accept() # conn = new socket object, addr = client address 
                print(f"Client connected: {addr}")

                client_handler = threading.Thread(target=self.handleClient, args=(conn, addr))
                client_handler.start()
        except KeyboardInterrupt:
            print("Stopped socket.")
            s.close()  

if __name__=="__main__":
    sc = ServerController()