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

# Buttons
host_rect = pygame.Rect((0,200), (100, 50)) # For positioning
join_rect = pygame.Rect((0, 20), (100, 50))
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