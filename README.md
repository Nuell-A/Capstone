# Capstone
Final project for CSC480.

### What is it?
My final project I decided to challenge myself with one that included technologies I was not familiar or comfortable with. It is a Kahoot-like game with online functionality where players can host or join live sessions. 

### Components
- Front-end 
	- The front-end will be created using Pygame/Pygame-GUI, this will include the GUI that will be used to interact with the game. There will be different screens for registration, quiz management, and live sessions. 
- Back-end 
	- The back-end will be written in Python and it will be composed of the game’s logic. This will include game logic such as score calculations, question and answer processing, and session management. 
- Database
	- Incorporating MySQL for the database system to store user accounts, quiz questions and answers, session data, and scoring. The purpose of using a database instead of built-in Python data structures is to ensure data integrity and to have consistent data functions. 
- Networking
	- In my opinion, the most difficult part. This is because I have never worked with anything like this before. At least, not at the “low level”. This component will enable online functionality, allowing client-server communication over the internet. This is the messenger between the user session and the server. 
- Security
	- This is more of a practice rather than a component, but just as important. This component will ensure that data for user accounts is secure and private. This will include encryption of data, and authorization of users to protect against unauthorized access.

### Purpose
The goal of this information system is to offer an alternative, but also interactive/engaging method to be incorporated in training programs. Although, this system could be used for a variety of things such as education. 
This system offers a platform that encourages user interaction and brings out their competitive side, but in a lighthearted manner while also offering some great educational opportunities.


### File Structure
Captstone/
│
├── src/
│   ├── client/
│   │   ├── assets/                 # Store graphical assets like images, fonts, etc.
│   │   ├── controllers/            # Logic for handling user inputs and events
│   │   ├── views/                  # User interface files for different screens
│   │   │   ├── menu.py             # Menu screen
│   │   │   ├── quiz.py             # Quiz screen
│   │   │   └── scoreboard.py       # Scoreboard screen
│   │   ├── models/                 # Classes representing data structures
│   │   └── utils/                  # Utility functions and constants
│   │       ├── constants.py        # Constants like colors, dimensions, etc.
│   │       └── helpers.py          # Helper functions
│   │
│   └── server/
│       ├── database/               # Database related files
│       │   ├── models.py           # ORM models or database schemas
│       │   └── db_connection.py    # Database connection setup
│       ├── controllers/            # Server logic to handle requests
│       │   ├── quiz_controller.py  # Handles quiz-related requests
│       │   └── user_controller.py  # Handles user-related requests
│       ├── utils/                  # Utility functions for server
│       └── server.py               # Main server script
│
├── tests/                          # Unit tests and integration tests
│   ├── client_tests/
│   └── server_tests/
│
├── config.py						# Configuration for SQL database and other sensitive information
│
├── venv/                           # Virtual environment
│
├── .gitignore                      # Specifies intentionally untracked files to ignore
├── requirements.txt                # List of dependencies for the project
└── README.md                       # Project overview and instructions