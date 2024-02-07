import pygame
import pygame_gui
from .base_view import BaseView
import time
import random


class QuizView(BaseView):
    '''Method displays the UI, controls events and the timer.'''

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object, player):
        super().__init__(screen, manager, screen_size, dt)
        self.ROUND_TIME = 3
        self.timer_duration = self.ROUND_TIME # Round duration
        self.start_time = None # timer control
        self.network_handler = network_handler
        self.questions = None
        self.used_question_dicts = []
        self.question_dicts = []
        self.wrong_answers = []
        self.player = player
        self.game_id = self.player.getGameID()
        self.selected_answer = None
        self.score = 0

    def createUI(self):
        '''Creates label, question, answer choices, and the score bar.'''
        # Timer
        self.timer_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 20), (50, 50)), text="45",
                                                  manager=self.manager,
                                                  container=None,
                                                  anchors={'centerx': 'centerx'}
                                                  )
        # Question box
        self.question_textbox = pygame_gui.elements.UILabel(text="Default Text", 
                                                         relative_rect=pygame.Rect((0, 50), (300, 100),),
                                                         manager=self.manager,
                                                         container=None,
                                                         anchors={'centerx': 'centerx', 'top_target': self.timer_label})
        # Answers choices 1-4 in a pnel.
        button_size = pygame.Rect((0, 0), (1200/4, 250)) # Button size of choices.
        self.answerchoice_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 50), (1200, 250)),
                                                         manager=self.manager,
                                                         starting_height=1,
                                                         container=None,
                                                         anchors={'centerx': 'centerx', 'top_target': self.question_textbox})
        self.answers = {}
        for i in range(4):
            button_rect = button_size.copy()
            button_rect.x = -10 + (1200/4 * i) # Button spacing
            button_rect.y = -3
            button_id = f"button{i}"
            self.answer_choice = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                                         text=f"Answer choice number {i}",
                                                         manager=self.manager,
                                                         container=self.answerchoice_panel,
                                                         )
            
            self.answers[button_id] = self.answer_choice
            
        # Live score bar
        self.score_bar = pygame_gui.elements.UIProgressBar(relative_rect=pygame.Rect((0, 50), (1200, 50)),
                                                      manager=self.manager,
                                                      container=None,
                                                      anchors={'centerx': 'centerx', 'top_target': self.answerchoice_panel})
        
    def killUI(self):
        self.timer_label.kill()
        self.question_textbox.kill()
        self.answerchoice_panel.kill()
        self.score_bar.kill()

        for answer_id, answer in self.answers.items():
            answer.kill()
        self.answers = {}
        
    def updateTimer(self):
        '''Method to control timer and check if has reached 0.'''
        # Calculate current time elapsed.
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) / 1000 # Converts from milliseconds to seconds.

        # Remaining time.
        remaining_time = max(self.timer_duration - elapsed_time, 0)
        self.timer_label.set_text(str(int(remaining_time)))

        # Checks if timer is done
        if remaining_time <= 0:
            self.timerDone()

    def resetTimer(self):
        self.timer_duration = self.ROUND_TIME
        self.start_time = pygame.time.get_ticks()

    def updateAnswers(self):
        '''Updates answer selections'''
        try:
            correct_answer = self.question_dicts[0]['correct_answer']
            selected_wrong_answers = random.sample(self.wrong_answers, 3)
            answer_choices = [correct_answer] + selected_wrong_answers
            random.shuffle(answer_choices)

            answer_key = 0
            for answer_id, answer in self.answers.items():
                answer.set_text(answer_choices[answer_key])
                answer_key += 1
        except IndexError:
            print("Answers are over")

    def updateQuestion(self):
        '''Updates question list'''
        try:
            next_question = self.question_dicts.pop(0)
            self.question_textbox.set_text(next_question['question_text'])
            
            self.used_question_dicts.append(next_question)
        except IndexError:
            print("Questions are over.")
            if not self.question_dicts:
                print("Changing to results")
                self.scene = "results"
                return "results"
            print(f"Active scene: {self.scene}")
            
    def timerDone(self):
        '''Resets timer, moves to next question in the set.'''
        self.checkAnswer()
        # Resets answer selection for new question/answer combo
        self.selected_answer = None
        self.resetTimer()
        self.updateAnswers()
        self.updateQuestion()
        

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                self.scene = "quit"
                return "quit"
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for button_id, button in self.answers.items():
                    if event.ui_element == button:
                        print(f"{button_id} selected: {button.text}")
                        self.selected_answer = {button.text}
                    
            self.manager.process_events(event)
        
        return True

    def handleResponse(self, response):
        if response['type'] == 'question_set_response':
            self.questions = response
            # List within list [[q_id, g_id, quesiton, answer], [q_id, g_id, quesiton, answer]]
            for question in self.questions['data'][0]['questions']:
                question_dict = {
                    'question_text': question[2],
                    'correct_answer': question[3],
                }

                self.question_dicts.append(question_dict)
            
            self.wrong_answers = response['data'][0]['wrong_answers']
        
        elif response['type'] == 'check_answer_response':
            score = response['data'][0]['score']
            self.player.setScore(score)
            print(f"Current score: {self.player}")


    def checkAnswer(self):
        '''Sends last selected asnwer to server and checks if it's correct or not.'''
        if self.selected_answer:
            selected_answer = list(self.selected_answer)
            print(selected_answer[0])
            print(self.game_id)
            request = {'type': 'check_answer', 'selected_answer': selected_answer[0], 'game_id': self.game_id}
            print("Sending answer to server.")
            self.network_handler.sendRequest(request)
            time.sleep(.2)
        else:
            selected_answer = self.selected_answer
            print(self.game_id)
            request = {'type': 'check_answer', 'selected_answer': selected_answer, 'game_id': self.game_id}
            print("Sending answer to server. NONE")
            self.network_handler.sendRequest(request)
            time.sleep(2)

    def getQuestionSet(self):
        "Requests uniqueID from server"
        request = {'type': 'question_set', 'game_id': self.game_id}
        print("Requesting question set: QUIZ")

        self.network_handler.sendRequest(request)
        time.sleep(.3)
        

    def update(self):
        '''Updates components that need to be updated.'''
        self.updateTimer()
        self.manager.update(self.dt)

    def sceneLoop(self):
        self.network_handler.setCallbackResponse(self.handleResponse)
        self.running = True
        self.getQuestionSet()
        print("creating UI quiz")
        self.createUI()
        self.updateAnswers() # Initial answer selection
        self.updateQuestion() # Places initial question
        self.start_time = pygame.time.get_ticks() # Initiates timer upon scene creation.

        while self.running:
            self.dt
            self.running = self.handleEvents()

            if self.scene == "quit":
                 return "quit"
            
            if self.scene == "results": # Temp
                self.killUI()
                print("killed ui")
                return "results"
            
            self.update()
            self.draw()

            pygame.display.update()