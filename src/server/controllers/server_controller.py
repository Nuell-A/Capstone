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
        self.active_sessions = {}
        self.question_sets = {}
        self.players = {}
        self.main()

    def sendResponse(self, conn, response):
        response_json = json.dumps(response)
        conn.sendall(response_json.encode('utf-8'))
        print("Sent RESPONSE.")

    def sendToSession(self, game_id, update):
        '''Sends an update (response, request, etc.) to clients in a game session.'''
        try:
            if game_id in self.active_sessions:
                print(f"Sending updates to clients in {game_id}")
                for client in self.active_sessions[game_id]:
                    conn = client['conn']
                    self.sendResponse(conn, update)
        except:
            print(f"There was an error updating clients for {game_id}")
            logging.error("Error updating session", exc_info=True)

        
    def processRequest(self, request, conn, addr):
        if request['type'] == "uniqueID":
            print("Creating unique ID....")
            response = self.gm.getUniqueID()
            game_id = response['data'][0]['uniqueID']
            name = request['data'][0]['name']
            response_questionset = self.gm.getQuestions(5)
            self.active_sessions[game_id] = [{'conn': conn, 'addr': addr}]
            self.question_sets[game_id] = response_questionset
            self.players[conn] = [{'name': name, 'score': 0}]
            print(self.question_sets)
            print(f"Hosting session with {addr}.\nCurrent active sessions: {self.active_sessions}")
            self.sendResponse(conn, response)

        elif request['type'] == "question_set":
            print("Getting question set...")
            game_id = request['game_id']
            response = self.question_sets[game_id]
            self.sendToSession(game_id, response)

        elif request['type'] == "join_request":
            print(f"JOIN REQUEST: {request}")
            game_id = request['data'][0]['game_id']
            name = request['data'][0]['name']
            print(f"Join request: game_id")
            if game_id: # Checks if game_id was passed
                self.joinSession(game_id, name, conn, addr)
            else:
                response = {'type': 'join_response', 'status': 'Error', 'message': 'Game ID not provided.'}
                self.sendResponse(conn, response)

        elif request['type'] == "start_request":
            print("Recieved update request.")
            game_id = request['game_id']
            update = {'type': 'start_response'}
            self.sendToSession(game_id, update)

        elif request['type'] == "check_answer":
            print("Checking answer")
            answer = request['selected_answer']
            game_id = request['game_id']
            print(game_id)
            questions = self.question_sets[game_id]['data'][0]['questions']

            for question in questions:
                correct_answer = question[3]
                if answer == correct_answer:
                    self.players[conn][0]['score'] +=10

            response = {'type': 'check_answer_response', 'data': [{'score': self.players[conn]}]}
            self.sendResponse(conn, response)

    def joinSession(self, game_id, name, conn, addr):
        if game_id in self.active_sessions:
            player_info = {'conn': conn, 'addr': addr}
            self.active_sessions[game_id].append(player_info)
            self.players[conn] = [{'name': name, 'score': 0}]
            print(f"Client {addr} joined AS.\nCurrent players: {self.players}\nCurrent active session: {self.active_sessions}")
            response = {'type': 'join_response', 'status': 'Success', 'message': 'Joined session.'}
            self.sendResponse(conn, response)
        else:
            response = {'type':'join_response', 'status': 'Error', 'message': 'Check game ID and try again.'}
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
                self.processRequest(request, conn, addr)
        except:
            logging.error("Error sending message", exc_info=True)
            
            conn.close()

        print("Client disconnected: " + str(addr))
        self.removePlayerFromSession(conn)
        print("Closing connection.")
        conn.close()

    def removePlayerFromSession(self, conn):
        print("Removing client from active session...")
        try:
            # Iterate over all key/values in the dictionary
            # game_id = game ID & client_list = [{conn, addr}, {conn, addr}, {}, ....]
            for game_id, client_list in self.active_sessions.items():
                # Finds the first dictionary that equals client being removed (conn)
                client_to_remove = next((client for client in client_list if client['conn'] == conn), None)
                # Remove the found dictionary from the list, if the client is there.
                if client_to_remove:
                    client_list.remove(client_to_remove)
            # Creates new active_sessions dict with remaining clinets (conns) and removes empty ones.
            self.active_sessions = {game_id: client_list for game_id, client_list in self.active_sessions.items() if client_list}
            print(f"Client removed. Current active sessions: {self.active_sessions}")
        except:
            print("There was an error removing client from active session. Check logs")
            logging.error("Error removing client from active session", exc_info=True)

    def main(self):
        self.db = Database()
        self.gm = GameManagement(self.db)
        print("Starting socket...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPV4 and TCP
        try:
            s.bind((config.socket_host, config.socket_port))
            s.listen()
            print("Socket binded successfully.")
            # Once accept is called it blocks script execution, hence why threading is needed.
            
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