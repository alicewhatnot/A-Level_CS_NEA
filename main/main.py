from core.parser import parse_expression
from core.graph_plotter import GraphPlotter
import pygame
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 600, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Input Box Example")

# Font and colors
font = pygame.font.SysFont(None, 36)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = text
        self.txt_surface = font.render(text, True, (0, 0, 0))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state if clicked
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = color_active if self.active else color_inactive

        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass  # We could trigger something here
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        # Draw text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Draw box
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text

# Create the input box
input_box = InputBox(50, 50, 300, 40)
user_input = ""  # Variable to store the user's text

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        input_box.handle_event(event)

        # Store latest user input when pressing Enter
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            user_input = input_box.get_text()
            try:
                ast_tree = parse_expression(user_input)  
                GraphPlotter.plot(ast_tree)        
            except Exception as e:
                print("Error parsing function:", e)

    # Draw the input box
    input_box.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
