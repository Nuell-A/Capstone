import pygame
import pygame_gui

running = True
WIDTH, HEIGHT = 1280, 720
clock = pygame.time.Clock() # Controls FPS and tracks time.
# dt = delta
dt = 0 

pygame.init()
pygame.display.set_caption("Menu")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color('#a575c6'))

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Buttons -----------------
# rects for positioning
host_rect = pygame.Rect((0,200), (100, 50))
join_rect = pygame.Rect((0, 20), (100, 50))
# Anchor targets are of the element being placed not the element you're placing next to.
#  e.g. in join_bt the top_target is the the top of join_bt to host_bt.
host_bt = pygame_gui.elements.UIButton(relative_rect=host_rect,
                                       text="Host",
                                       manager=manager,
                                       container=None,
                                       anchors={'centerx': 'centerx'})
join_bt = pygame_gui.elements.UIButton(relative_rect=join_rect,
                                       text="Join",
                                       manager=manager,
                                       container=None,
                                       anchors={'centerx': 'centerx',
                                                'top_target': host_bt})

# Label
title_label = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 50), (150, 100)),
                                         html_text='<h1><effect id=title>GAME TITLE</effect></h1>',
                                         manager=manager,
                                         container=None,
                                         anchors={'centerx': 'centerx'})
title_label.set_active_effect(pygame_gui.TEXT_EFFECT_BOUNCE, effect_tag='title')

# TextBox
usrname_text = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((0,80), (250, 50)),
                                                  initial_text="Type user name here.....",
                                                  manager=manager,
                                                  container=None,
                                                  anchors={'centerx': 'centerx', 
                                                           'top_target': join_bt})

while running:
    dt = clock.tick(30) / 1000 # Limited to 30 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == host_bt:
                print("Hosting session...")
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == join_bt:
                print("Joining session...")

        manager.process_events(event)

    manager.update(dt)

    # blit is used to add a surface to the screen.
    screen.blit(background, (0, 0))
    manager.draw_ui(screen)

    pygame.display.update() # Updates the whole screen (if no argument is passed).

pygame.quit()