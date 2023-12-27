import pygame
import pygame_gui

SCREEN = (1280, 720)

class QuizView:
    '''Live quiz view elements.'''

    def __init__(self, manager, window):
        self.manager = manager
        self.window = window
        self.createUI()

    def createUI(self):
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
        answers = {}
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
            
            answers[button_id] = self.answer_choice
            
        # Live score bar
        self.score_bar = pygame_gui.elements.UIProgressBar(relative_rect=pygame.Rect((0, 50), (1200, 50)),
                                                      manager=self.manager,
                                                      container=None,
                                                      anchors={'centerx': 'centerx', 'top_target': self.answerchoice_panel})

    def handleEvents(self, event):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.choice1:
                    print("Answer choice 1 selected.")
                if event.ui_element == self.choice2:
                    print("Answer choice 2 selected.")
                if event.ui_element == self.choice3:
                    print("Answer choice 3 selected.")
                if event.ui_element == self.choice4:
                    print("Answer choice 4 selected.")
            
        self.manager.process_events(event)

    def update(self, dt):
        self.manager.update(dt)

    def draw(self):
        background = pygame.Surface(SCREEN)
        background.fill(pygame.Color('#a575c6'))

        # blit is used to add a surface to the screen.
        self.window.blit(background, (0, 0))
        self.manager.draw_ui(self.window)

def main():
    '''Main loop.'''
    running = True
    clock = pygame.time.Clock()
    dt = 0

    pygame.init()
    pygame.display.set_caption("Game Session")
    window = pygame.display.set_mode(SCREEN)
    manager = pygame_gui.UIManager(SCREEN)

    quiz_view = QuizView(manager, window)

    while running:
        dt = clock.tick(30)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            quiz_view.handleEvents(event)

        quiz_view.update(dt)
        quiz_view.draw()
        pygame.display.update()

    pygame.quit()

if __name__=="__main__":
    main()
