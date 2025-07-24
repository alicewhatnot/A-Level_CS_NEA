import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Function Input Box")

font = pygame.font.SysFont(None, 36)
input_box = pygame.Rect(50, 20, 300, 40)
submit_button = pygame.Rect(370, 20, 100, 40)

color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color_button = pygame.Color('gray60')
color = color_inactive
active = False
text = ''
function_to_draw = "x"

def draw_button(screen, rect, text):
    pygame.draw.rect(screen, color_button, rect)
    txt_surf = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surf, (rect.x + 10, rect.y + 8))

def evaluate_function(func_str, x_val):
    try:
        x = x_val
        return eval(func_str)
    except Exception:
        return None

def draw_function(screen, func_str):
    points = []
    for px in range(WIDTH):
        x = (px - WIDTH // 2) / 40
        y = evaluate_function(func_str, x)
        if y is not None and abs(y) < 100:
            py = HEIGHT // 2 - int(y * 40)
            points.append((px, py))
    if len(points) > 1:
        pygame.draw.aalines(screen, (50, 150, 255), False, points)

clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))

    draw_function(screen, function_to_draw)
    draw_button(screen, submit_button, "Submit")

    txt_surface = font.render(text, True, (0, 0, 0))
    width = max(300, txt_surface.get_width()+10)
    input_box.w = width
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive

            if submit_button.collidepoint(event.pos):
                function_to_draw = text  # Update function string

        elif event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_RETURN:
                function_to_draw = text
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
