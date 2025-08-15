import pygame

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 600

# Font
FONT = pygame.font.SysFont(None, 28)

# Colors
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_BUTTON = pygame.Color('gray60')
COLOR_CHECKBOX_BORDER = pygame.Color('black')
COLOR_CHECKBOX_FILL = pygame.Color('green')

# Backgrounds
BG_COLOR = (255, 255, 255)
SIDEBAR_COLOR = (230, 230, 230)

# Frame rate
FPS = 60
