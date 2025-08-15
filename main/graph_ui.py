import pygame
from settings import WIDTH, HEIGHT

def drawGraphArea(screen):
    """Draws the graph background and axes."""
    # Graph area rectangle
    graph_rect = pygame.Rect(300, 0, WIDTH - 300, HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), graph_rect)

    # Axis lines
    center_x = 300 + (WIDTH - 300) // 2
    center_y = HEIGHT // 2
    pygame.draw.line(screen, (100, 100, 100), (center_x, 0), (center_x, HEIGHT), 2)  # y-axis
    pygame.draw.line(screen, (100, 100, 100), (300, center_y), (WIDTH, center_y), 2)  # x-axis
