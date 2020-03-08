import pygame

from settings import Settings
from button import Button
from graph import Graph
import functions as f


def run_simulation():
    # Initialize game and create a screen object.
    pygame.init()
    settings = Settings() 
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Cylinder Puzzle")
    
    # Make buttons.
    random_button = Button(settings, screen, "Randomize", -100, 300, 200)
    run_button = Button(settings, screen, "Run", 100, 300, 100)
    
    #make graph
    graph = Graph(settings,screen)
    
    # Start the main loop for the game.
    while True:
        f.check_events(settings, screen, random_button, run_button, graph)
        f.update_screen(settings, screen, random_button, run_button, graph)
                 
       

run_simulation()




