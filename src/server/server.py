import socket
import threading
import json
import random

import sys
sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")
sys.path.insert(2, "C:\\Users\\alcal\\Documents\\Projects\\Capstone\\Capstone\\src") # Windows
import config



'''This file will handle the hosting of the server on the itnernet.

JSON communication protocol:
types - request_question_set, question_set | join_session, join_session_response | unique_id, unique_id_response

Example:
{
    "type": "request_question_set,
    "data": {
        "questions": [
            {
                "text": "question",
                "options": ["answer1", "answer2", "answer3", "answer4"],
                "correct_option": "answer2"
            },
            {
                "text": "question2",
                // Fill in the rest.
            }
        ]
    },
}'''

def handleClient(conn, addr):
    try:
        print(f"handling client: {addr}")
        while True:
            data = conn.recv(2048)
            
            if not data:
                break
            
            request = data.decode('utf-8')
            request_load = json.loads(request)

            print(f"Received data: {request_load}")

            conn.sendall("message received".encode('utf-8'))
    except:
        print("Closing connection.")
        return
    
    print("Client disconnected: " + str(addr))

def getQuestionSet():
    '''Gets questions from database and returns question set in JSON format.'''

    return "Question set delivered"

def getUniqueID(request):
    '''Gets uniqueID and returns it in JSON format.'''

    print("Creating Unique ID:")
    game_id = ""
    x = random.randint(100000, 999999)
    game_id = str(x)

    response = {
        'type': 'uniqueID_response',
        'data': [{
            'uniqueID': game_id
        }]
    }

    return response

def checkJoinSession():
    '''Takes game ID from request and checks it against database (if it exists).
    Returns approve or denied (if not exists)'''
    return "Joined session"

def main():
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

            client_handler = threading.Thread(target=handleClient, args=(conn, addr))
            client_handler.start()
    except KeyboardInterrupt:
        print("Stopped socket.")
        s.close()  

if __name__=="__main__":
    main()