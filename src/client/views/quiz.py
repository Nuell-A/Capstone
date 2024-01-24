import pygame
import pygame_gui
from .base_view import BaseView



class QuizView(BaseView):
    '''Method displays the UI, controls events and the timer.'''

    def __init__(self, screen, manager, screen_size: tuple, dt, network_handler: object):
        super().__init__(screen, manager, screen_size, dt)
        self.timer_duration = 45 # Round duration
        self.start_time = None # timer controla
        self.network_handler = network_handler

    def createUI(self):
        '''Creates label, question, answer choices, and the score bar.'''
        # Timer
        self.timer_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 20), (50, 50)), text="45",
                                                  manager=self.manager,
                                                  container=None,
                                                  anchors={'centerx': 'centerx'}
                                                  )
        # Question box
        self.question_textbox = pygame_gui.elements.UITextBox(html_text='<p>Questions will go here, understand?</p>', 
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

    def timerDone(self):
        '''Will have more in the future.'''
        print("Ding ding ding ding...")
        # Implement next question and answers combo
        # Reset timer

    def handleEvents(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quitting")
                    self.scene = "quit"
                    return "quit"
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    for button_id, button in self.answers.items():
                        if event.ui_element == button:
                            # Implement switchcase or if-elif blocks for each button_id and check if choice is correct/wrong
                            print(f"1Answer choice {button_id} selected.")
                        
                    
                self.manager.process_events(event)
            
            return True

    def getQuestionSet(self):
        "Requests uniqueID from server"
        request = {'type': 'question_set'}
        print("Requesting question set: QUIZ")

        self.network_handler.sendRequest(request)

    def update(self):
        '''Updates components that need to be updated.'''
        self.updateTimer()
        self.manager.update(self.dt)

    def sceneLoop(self):
        self.running = True
        self.getQuestionSet()
        print("creating UI quiz")
        self.createUI()
        self.start_time = pygame.time.get_ticks() # Initiates timer upon scene creation.

        while self.running:
            self.dt
            self.running = self.handleEvents()
            if self.running == "quit":
                 return "quit"
            
            if self.running == "quiz": # Temp
                self.killUI()
                print("killed ui")
                return
            
            self.update()
            self.draw()

            pygame.display.update()