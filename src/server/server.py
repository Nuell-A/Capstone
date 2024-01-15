import socket
import threading
import sys
import time

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

def socketStart():
    print("Starting socket...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

        request = conn.recv(1024).decode("utf-8")

        if request == "hosting":
            pass


    """socket_listen = threading.Thread(target=socketStart)
    socket_listen.start()

    test = threading.Thread(target=testFunction)
    test.start()"""
