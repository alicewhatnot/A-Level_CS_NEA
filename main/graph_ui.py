import pygame
import math
from settings import WIDTH, HEIGHT, SIDEBAR_WIDTH, GRAPH_FONT, GRAPH_AXIS_FONT, COLOUR_BACKGROUND

def drawGraphArea(screen, derivative_order=1, dual_view=False, variable="x",font=[GRAPH_FONT, GRAPH_AXIS_FONT], scale=40, use_degrees=False):
    """Draws the graph background and axes with dynamic numbering. Supports degree X-axis for trig functions."""
    axis_color = (50, 50, 50)
    grid_color = (200, 200, 200)

    def draw_axes(center_x, center_y, left, top, width, height, bottom_graph=False,
                  clip_bottom=None, scale=40, font=[GRAPH_FONT, GRAPH_AXIS_FONT], use_degrees=False):
        y_axis_bottom = top + height if clip_bottom is None else clip_bottom
        pygame.draw.line(screen, axis_color, (center_x, top), (center_x, y_axis_bottom), 2)
        pygame.draw.line(screen, axis_color, (left, center_y), (left + width, center_y), 2)

        # Axis labels
        if bottom_graph:
            y_label = f"f{'\'' * derivative_order}({variable})"
        else:
            y_label = f"f{'\'' * (derivative_order - 1)}({variable})"

        x_text = font[1].render(variable, True, axis_color)
        y_text = font[1].render(y_label, True, axis_color)
        x_label_rect = x_text.get_rect(topleft=(left + width - x_text.get_width() - 10, center_y))
        y_label_rect = y_text.get_rect(topleft=(center_x + 8, top + 5))
        screen.blit(x_text, x_label_rect.topleft)
        screen.blit(y_text, y_label_rect.topleft)

        # X-axis numbers
        if use_degrees:
            # Multiples of 90 or pi/2 radians
            step_radians = math.pi / 2
            num_steps = (width // scale) // 2
            for n in range(-num_steps, num_steps + 1):
                if n == 0:
                    continue
                rad_value = n * step_radians
                px = center_x + rad_value * scale
                deg_label = int(math.degrees(rad_value))
                text = font[0].render(str(deg_label), True, axis_color)
                text_rect = text.get_rect(center=(px, center_y + 8 + text.get_height()//2))
                if text_rect.colliderect(x_label_rect):
                    continue
                screen.blit(text, text_rect.topleft)
        else:
            # Normal integer units
            num_x_ticks = width // scale
            for i in range(-num_x_ticks//2, num_x_ticks//2 + 1):
                if i == 0 or i == -num_x_ticks//2 or i == num_x_ticks//2:
                    continue
                x = center_x + i * scale
                text = font[0].render(str(i), True, axis_color)
                text_rect = text.get_rect(center=(x, center_y + 8 + text.get_height()//2))
                if text_rect.colliderect(x_label_rect):
                    continue
                screen.blit(text, text_rect.topleft)

        # Y-axis numbers
        num_y_ticks = height // scale
        for i in range(-num_y_ticks//2, num_y_ticks//2 + 1):
            if i == 0:
                continue
            y = center_y - i * scale
            text = font[0].render(str(i), True, axis_color)
            text_rect = text.get_rect(center=(center_x + 8 + text.get_width()//2, y))
            if text_rect.colliderect(y_label_rect):
                continue
            screen.blit(text, text_rect.topleft)

    # Draw graph(s)
    if not dual_view:
        graph_rectangle = pygame.Rect(SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEIGHT)
        pygame.draw.rect(screen, COLOUR_BACKGROUND, graph_rectangle)
        center_x = SIDEBAR_WIDTH + (WIDTH - SIDEBAR_WIDTH)//2
        center_y = HEIGHT//2
        draw_axes(center_x, center_y, SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEIGHT,
                  scale=scale, font=font, use_degrees=use_degrees)
    else:
        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        graph_height = HEIGHT // 2
        separator_gap = 4

        # Top half
        top_center_x = graph_left + graph_width // 2
        top_center_y = graph_height // 2
        pygame.draw.rect(screen, COLOUR_BACKGROUND, (graph_left, 0, graph_width, graph_height))
        draw_axes(top_center_x, top_center_y, graph_left, 0, graph_width, graph_height,
                  clip_bottom=graph_height - separator_gap, scale=scale, font=font, use_degrees=False)

        # Bottom half
        bottom_center_x = graph_left + graph_width // 2
        bottom_center_y = graph_height + graph_height // 2
        pygame.draw.rect(screen, COLOUR_BACKGROUND, (graph_left, graph_height, graph_width, graph_height))
        draw_axes(bottom_center_x, bottom_center_y, graph_left, graph_height + separator_gap,
                  graph_width, graph_height, bottom_graph=True, clip_bottom=HEIGHT,
                  scale=scale, font=font, use_degrees=False)

        # Separator lines
        pygame.draw.line(screen, grid_color, (graph_left, graph_height - separator_gap),(WIDTH, graph_height - separator_gap), 1)
        pygame.draw.line(screen, grid_color, (graph_left, graph_height + separator_gap),(WIDTH, graph_height + separator_gap), 1)
