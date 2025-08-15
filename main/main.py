from core.function_entry import FunctionEntry
from core.graph_plotter import GraphPlotter
import pygame
import sys

from settings import WIDTH, HEIGHT, BG_COLOR, SIDEBAR_COLOR, FPS
from ui_elements import InputBox, Checkbox, Button
from graph_ui import drawGraphArea

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Function Transformation UI")

# UI Elements
function_box = InputBox(20, 20, 200, 32, "Enter function")
submit_func_button = Button(20, 40, 160, 32, "Submit")

x_stretch_box = InputBox(20, 70, 60, 32, "1")
y_stretch_box = InputBox(100, 70, 60, 32, "1")
x_shift_box = InputBox(20, 120, 60, 32, "0")
y_shift_box = InputBox(100, 120, 60, 32, "0")

reflect_x = Checkbox(20, 170, "Reflect X-axis")
reflect_y = Checkbox(20, 200, "Reflect Y-axis")

submit_trans_button = Button(20, 300, 200, 40, "Submit Transformations")

# User Inputs
user_function = ""
transform_values = {"x_stretch": 1, "y_stretch": 1, "x_shift": 0, "y_shift": 0}
reflection_values = {"reflect_x": False, "reflect_y": False}

# Main loop 
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, SIDEBAR_COLOR, (0, 0, 300, HEIGHT))

    drawGraphArea(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        function_box.handleEvent(event)
        x_stretch_box.handleEvent(event)
        y_stretch_box.handleEvent(event)
        x_shift_box.handleEvent(event)
        y_shift_box.handleEvent(event)
        reflect_x.handleEvent(event)
        reflect_y.handleEvent(event)

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and function_box.active) or (submit_func_button.isClicked(event)):
            user_function = function_box.getText()
            user_function = FunctionEntry(user_function) 
            user_function.parseFunction()
            user_function.functionAST()
            function_tree = user_function.outputFunction()

        if submit_trans_button.isClicked(event):
            transform_values["x_stretch"] = x_stretch_box.getText()
            transform_values["y_stretch"] = y_stretch_box.getText()
            transform_values["x_shift"] = x_shift_box.getText()
            transform_values["y_shift"] = y_shift_box.getText()
            reflection_values["reflect_x"] = reflect_x.getValue()
            reflection_values["reflect_y"] = reflect_y.getValue()
            print("Transformations:", transform_values)
            print("Reflections:", reflection_values)

    # Draw all UI elements
    function_box.draw(screen)
    submit_func_button.draw(screen)
    x_stretch_box.draw(screen)
    y_stretch_box.draw(screen)
    x_shift_box.draw(screen)
    y_shift_box.draw(screen)
    reflect_x.draw(screen)
    reflect_y.draw(screen)
    submit_trans_button.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()


