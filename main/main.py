from core.function_entry import FunctionEntry
from core.graph_plotter import GraphPlotter
import pygame
import sys

from settings import WIDTH, HEIGHT, BG_COLOR, SIDEBAR_COLOR, FPS
from ui_elements import InputBox, Checkbox, Button, Text
from graph_ui import drawGraphArea

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Function Transformation UI")

# UI Elements
function_text = Text(20,30, "Enter Function")
y_text = Text(20,66, "y =")
function_box = InputBox(55, 60, 200, 40)
submit_func_button = Button(230, 60, 90, 40, "Submit")

in_x_axis = Text(20, 120, "X Axis")
x_stretch_text = Text(20, 150, "Stretch scale factor")
x_stretch_box = InputBox(220, 145, 32, 32, "1")

x_shift_text = Text(20, 190, "Shift amount")
x_shift_box = InputBox(220, 185, 32, 32, "0")

x_reflect_text = Text(20, 230, "Reflect X-axis")
x_reflect = Checkbox(220, 230)

in_y_axis = Text(20, 280, "Y Axis")

y_stretch_text = Text(20, 310, "Stretch scale factor")
y_stretch_box = InputBox(220, 305, 32, 32, "1")

y_shift_text = Text(20, 350, "Shift amount")
y_shift_box = InputBox(220, 345, 32, 32, "0")

y_reflect_text = Text(20, 390, "Reflect Y-axis")
y_reflect = Checkbox(220, 390)

submit_trans_button = Button(20, 430, 300, 40, "Submit Transformations")

# User Inputs
user_function = ""
transform_values = {"x_stretch": 1, "y_stretch": 1, "x_shift": 0, "y_shift": 0}
reflection_values = {"x_reflect": False, "y_reflect": False}

# Main loop 
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, SIDEBAR_COLOR, (0, 0, 400, HEIGHT))

    drawGraphArea(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        function_box.handleEvent(event)
        x_stretch_box.handleEvent(event)
        y_stretch_box.handleEvent(event)
        x_shift_box.handleEvent(event)
        y_shift_box.handleEvent(event)
        x_reflect.handleEvent(event)
        y_reflect.handleEvent(event)

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
            reflection_values["reflect_x"] = x_reflect.getValue()
            reflection_values["reflect_y"] = y_reflect.getValue()
            print("Transformations:", transform_values)
            print("Reflections:", reflection_values)

    # Draw all UI elements
    function_text.draw(screen)
    y_text.draw(screen)
    function_box.draw(screen)
    submit_func_button.draw(screen)

    in_x_axis.draw(screen)
    x_stretch_text.draw(screen)
    x_stretch_box.draw(screen)
    x_shift_text.draw(screen)
    x_shift_box.draw(screen)
    x_reflect_text.draw(screen)
    x_reflect.draw(screen)

    in_y_axis.draw(screen)
    y_stretch_text.draw(screen)
    y_stretch_box.draw(screen)
    y_shift_text.draw(screen)
    y_shift_box.draw(screen)
    y_reflect_text.draw(screen)
    y_reflect.draw(screen)

    submit_trans_button.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()


