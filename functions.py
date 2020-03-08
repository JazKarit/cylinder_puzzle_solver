import sys
from time import sleep

import json
import pygame

        

def check_random_button(settings, screen, button,mouse_x,mouse_y,graph):
    """Randomize balls"""
    button_clicked = button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked:
        graph.randomize()
        
def check_run_button(settings,screen,button,mouse_x,mouse_y,graph):
    """Run algorithm"""
    button_clicked = button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked:
        #print(graph.search_ball(1,1))
        #graph.move_ball_node(6,7)
        #graph.solve_node(1,1)
        graph.solve_puzzle()

def check_events(settings, screen, random_button, run_button,graph):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_random_button(settings, screen, random_button,mouse_x,mouse_y,graph)
            check_run_button(settings, screen, run_button,mouse_x,mouse_y,graph)
            
def update_screen(settings, screen, random_button, run_button, graph):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(settings.bg_color)
    random_button.draw_button()
    run_button.draw_button()
    graph.draw_graph()
    
    # Make the most recently drawn screen visible.
    pygame.display.flip()
