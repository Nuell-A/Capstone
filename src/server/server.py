import socket
import threading
import json

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

def handleClient(conn):
    try:
        while True:
            data = conn.recv(1024)

            if not data: # Checks for client connection
                break
            
            request = json.loads(data.decode('utf-8')) # Load JSON file (request)
            request_type = request.get('type', '') # .get(key, default_value)
            # Below is handling of requests with threads.
            if request_type == "request_question_set":
                response = getQuestionSet()
                return response

            elif request_type == "join_session":
                response = checkJoinSession()
                return response

            elif request_type == "unique_id":
                response = getUniqueID()
                return response
            
    except Exception as e:
        print(f"There was an error handling the client: {e}")

    finally:
        conn.close() # Always closes socket connection

def getQuestionSet():
    '''Gets questions from database and returns question set in JSON format.'''

    return "Question set delivered"

def getUniqueID():
    '''Gets uniqueID and returns it in JSON format.'''
    return "Unique ID delivered"

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
    except:
        print("There was an error starting the socket.")
        s.close()
    
    
    print("Ready to accept clients:")
    while True:
        conn, addr = s.accept() # conn = new socket object, addr = client address 
        print(f"Client connected: {addr}")

        client_handler = threading.Thread(target=handleClient, args=(conn, ))
        client_handler.start()
        