import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.insert(1, "/Users/emanuelalcala/Desktop/Projects/Project/Capstone/src")
sys.path.insert(2, "C:\\Users\\alcal\\Documents\\Projects\\Capstone\\Capstone\\src")
from server.controllers.server_controller import ServerController

class TestServerController(unittest.TestCase):

    def setUp(self) -> None:
        self.server_controller = ServerController()

    def test_handleChatRequest_calls_sendToSession(self):
        # Arrange
        request = {'game_id': 'some_id', 'message': 'Hello, world!'}
        conn = MagicMock()
        
        # Patch the players dictionary with mock data
        self.server_controller.players = {conn: [{'name': 'Player1', 'score': 0}]}
        
        # Patch the sendToSession method
        with patch.object(self.server_controller, 'sendToSession') as mock_sendToSession:
            # Act
            self.server_controller.handleChatRequest(request, conn)
            
            # Assert
            mock_sendToSession.assert_called_once_with('some_id', {'type': 'chat_response', 'data': [{'name': 'Player1', 'message': 'Hello, world!'}]})
        
    def test_handleJoinRequestSuccess(self):
        # Mock request without game_id
        request = {'type': 'join_request', 'data': [{'name': 'Player1', 'game_id': '123456'}]}
        conn = MagicMock()
        test_conn = MagicMock()
        addr = "127.0.0.1"
        self.server_controller.active_sessions={'123456': [{'conn': test_conn, 'addr': '127.0.0.1'}]}

        # Call method
        self.server_controller.handleJoinRequest(request, conn, addr)

        # Checks if sendResponse parameter was called with...
        self.assertTrue('123456' in self.server_controller.active_sessions)
        self.assertEqual(len(self.server_controller.active_sessions['123456']), 2)
        self.assertTrue(conn in self.server_controller.players)
        self.assertEqual(self.server_controller.players[conn][0]['name'], 'Player1')
        self.assertEqual(self.server_controller.players[conn][0]['score'], 0)

    def test_handleUniqueIDRequest(self):
        # Mock instance of GameManagement
        mock_game_management = MagicMock()
        mock_game_management.getUniqueID.return_value = {'data': [{'uniqueID': '123456'}]}
        mock_game_management.getQuestions.return_value = [{'question1': 'What is your name?'}]

        # Create a mock connection and address
        mock_conn = MagicMock()
        mock_addr = ('localhost', 1234)

        # Create an instance of ServerController
        self.server_controller.gm = mock_game_management

        # Create a mock request
        mock_request = {'type': 'uniqueID', 'data': [{'name': 'Player1'}]}

        # Call the method
        self.server_controller.handleUniqueIDRequest(mock_request, mock_conn, mock_addr)

        # Assertions
        self.assertIn('123456', self.server_controller.active_sessions)  # Check if game_id is in active_sessions
        self.assertIn('123456', self.server_controller.question_sets)  # Check if game_id is in question_sets
        self.assertIn(mock_conn, self.server_controller.players)  # Check if conn is in players
        self.assertEqual(self.server_controller.players[mock_conn][0]['name'], 'Player1')  # Check if player name is correct


    

if __name__ == "__main__":
    unittest.main()