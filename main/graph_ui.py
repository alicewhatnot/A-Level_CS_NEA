import pygame
from settings import WIDTH, HEIGHT, SIDEBAR_WIDTH

def drawGraphArea(screen):
    """Draws the graph background and axes."""
    # Graph area rectangle
    graph_rect = pygame.Rect(SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), graph_rect)

    # Center of the graph area 
    center_x = SIDEBAR_WIDTH + (WIDTH - SIDEBAR_WIDTH) // 2
    center_y = HEIGHT // 2

    # Axis lines
    pygame.draw.line(screen, (100, 100, 100), (center_x, 0), (center_x, HEIGHT), 2)  # y-axis
    pygame.draw.line(screen, (100, 100, 100), (SIDEBAR_WIDTH, center_y), (WIDTH, center_y), 2)  # x-axis
