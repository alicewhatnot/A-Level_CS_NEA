import pygame
from settings import WIDTH, HEIGHT, SIDEBAR_WIDTH

def drawGraphArea(screen, dual_view=False):
    """Draws the graph background and axes. Supports split view."""
    if not dual_view:
        # Single full-height graph
        graph_rect = pygame.Rect(SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), graph_rect)

        center_x = SIDEBAR_WIDTH + (WIDTH - SIDEBAR_WIDTH) // 2
        center_y = HEIGHT // 2

        pygame.draw.line(screen, (100, 100, 100), (center_x, 0), (center_x, HEIGHT), 2)  # y-axis
        pygame.draw.line(screen, (100, 100, 100), (SIDEBAR_WIDTH, center_y), (WIDTH, center_y), 2)  # x-axis

    else:
        # Two half-height graphs
        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        graph_height = HEIGHT // 2

        # --- Top half ---
        top_rect = pygame.Rect(graph_left, 0, graph_width, graph_height)
        pygame.draw.rect(screen, (255, 255, 255), top_rect)

        top_center_x = graph_left + graph_width // 2
        top_center_y = graph_height // 2
        pygame.draw.line(screen, (100, 100, 100), (top_center_x, 0), (top_center_x, graph_height), 2)
        pygame.draw.line(screen, (100, 100, 100), (graph_left, top_center_y), (WIDTH, top_center_y), 2)

        # --- Bottom half ---
        bottom_rect = pygame.Rect(graph_left, graph_height, graph_width, graph_height)
        pygame.draw.rect(screen, (255, 255, 255), bottom_rect)

        bottom_center_x = graph_left + graph_width // 2
        bottom_center_y = graph_height + graph_height // 2
        pygame.draw.line(screen, (100, 100, 100), (bottom_center_x, graph_height), (bottom_center_x, HEIGHT), 2)
        pygame.draw.line(screen, (100, 100, 100), (graph_left, bottom_center_y), (WIDTH, bottom_center_y), 2)
