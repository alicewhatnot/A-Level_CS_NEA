from core.function_entry import FunctionEntry
from core.graph_plotter import GraphPlotter
from core.function import Function 
from core.transform_manager import TransformManager 
import pygame
import sys

from settings import WIDTH, HEIGHT, BG_COLOR, SIDEBAR_COLOR, SIDEBAR_WIDTH, FPS
from ui_elements import InputBox, Checkbox, Button, Text
from graph_ui import drawGraphArea

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Function Transformation UI")

# UI Elements
function_text = Text(20,30, "Enter Function")
y_text = Text(20,66, "y =")
function_box = InputBox(55, 60, 165, 40)
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

user_function_text = ""

# Main loop 
clock = pygame.time.Clock()
running = True

graph_plotter = GraphPlotter()
function_entered = False

while running:
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, SIDEBAR_COLOR, (0, 0, SIDEBAR_WIDTH, HEIGHT))

    drawGraphArea(screen)
    
    if graph_plotter.current_graph is not None:
        graph_plotter.plotSubsequent(screen, graph_plotter.current_graph)

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
            user_function_text = function_box.getText()
            user_function_entry = FunctionEntry(user_function_text) 
            user_function_entry.parseFunction()
            user_function_entry.functionAST()
            function_tree = user_function_entry.outputFunction()
            function_object = Function(function_tree)  # changed from expression_object
            graph_plotter.plotFunction(screen, function_object)  # assuming plotExpression → plotFunction
            function_entered = True
            transform_manager = TransformManager(function_object)

        if submit_trans_button.isClicked(event) and function_entered:

            transform_manager.addTransformations(
            x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
            )
            print ("Transformations Enqueued")
            transform_manager.applyAllTransformations(graph_plotter, screen)
            print ("Transformations Applied")

            function_object = transform_manager.getCurrentFunction()

            
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
