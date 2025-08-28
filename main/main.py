from core.function_entry import FunctionEntry
from core.graph_plotter import GraphPlotter
from core.function import Function 
from core.transform_manager import TransformManager 
from core.animation_controller import AnimationController
from core.queue import Queue
import pygame
import os
import sys

from settings import WIDTH, HEIGHT, SIDEBAR_WIDTH, FPS, MATHS_FONT, COLOUR_BACKGROUND, COLOUR_SIDEBAR, COLOUR_INACTIVE, COLOUR_FAIL
from ui_elements import InputBox, Checkbox, Button, Text
from graph_ui import drawGraphArea

pygame.init()
pygame.key.set_repeat(300, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Function Transformation UI")

from settings import load_assets
arrow_img, tick_img = load_assets()

# UI Elements
function_text = Text(20,30, "Enter Function")
y_text = Text(20,66, "f(x) =")
function_box = InputBox(75, 60, 155, 40, font=MATHS_FONT)
submit_func_button = Button(235, 60, 90, 40, "Submit")

differentiate_button = Button(20, 120, 140, 32, "Differentiate")

in_x_axis = Text(20, 120, "X Axis")
x_stretch_text = Text(20, 150, "Stretch scale factor")
x_stretch_box = InputBox(220, 145, 48, 32, text="1", center_text=True)

x_reflect_text = Text(20, 190, "Reflect X-axis")
x_reflect = Checkbox(220, 185, 48, 32, tick_img=tick_img)

x_shift_text = Text(20, 230, "Shift amount")
x_shift_box = InputBox(220, 225, 48, 32, text="0", center_text=True)

in_y_axis = Text(20, 280, "Y Axis")

y_stretch_text = Text(20, 310, "Stretch scale factor")
y_stretch_box = InputBox(220, 305, 48, 32, text="1", center_text=True)

y_reflect_text = Text(20, 350, "Reflect Y-axis")
y_reflect = Checkbox(220, 345, 48, 32, tick_img=tick_img)

y_shift_text = Text(20, 390, "Shift amount")
y_shift_box = InputBox(220, 385, 48, 32, text="0", center_text=True)

submit_trans_button = Button(20, 430, 305, 40, "Submit Transformations")

user_function_text = ""

transformation_tab_button = Button(20, HEIGHT - 60, 140, 40, "Transform")
differentiation_tab_button = Button(180, HEIGHT - 60, 140, 40, "Differentiate")

transform_to_ui = {
    ("stretch", "x"): x_stretch_box.rect,
    ("stretch", "y"): y_stretch_box.rect,
    ("shift", "x"): x_shift_box.rect,
    ("shift", "y"): y_shift_box.rect,
    ("reflect", "x"): x_reflect.rect,
    ("reflect", "y"): y_reflect.rect
}

# Main loop 
clock = pygame.time.Clock()
running = True

graph_plotter = GraphPlotter()
animation_controller = AnimationController(graph_plotter, duration=2000)  # 1s per transformation
function_entered = False
current_tab = "transformations"
previous_transformations = []
current_displayed_function = None

while running:
    screen.fill(COLOUR_BACKGROUND)
    pygame.draw.rect(screen, COLOUR_SIDEBAR, (0, 0, SIDEBAR_WIDTH, HEIGHT))

    if current_tab == "differentiation":
        drawGraphArea(screen, dual_view=True)
    else:
        drawGraphArea(screen, dual_view=False)

    # If a function has been entered, update animation controller
    if function_entered:
        dual_view = (current_tab == "differentiation")
        animation_controller.update(screen, dual_view=dual_view)

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

        # Submit new function
        if ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and function_box.active) 
            or submit_func_button.isClicked(event)):

            user_function_text = function_box.getText()
            user_function_entry = FunctionEntry(user_function_text) 
            success = user_function_entry.parseFunction()

            if not success:
                function_box.border_colour = COLOUR_FAIL
            else:
                function_box.border_colour = COLOUR_INACTIVE

                user_function_entry.functionAST()
                function_tree, function_variable = user_function_entry.outputFunction()
                function_object = Function(function_tree, function_variable)

                graph_plotter.plotFunction(function_object)  
                function_entered = True
                current_displayed_function = function_object

                # Reset managers
                transform_manager = TransformManager(function_object)
                animation_controller.queue.clear()
                animation_controller.animating = False
                animation_controller.current_function = None
                previous_transformations = None


        # Submit transformations
        if submit_trans_button.isClicked(event) and function_entered:

            # Always clear and enqueue, even if unchanged
            animation_controller.queue.clear()
            animation_controller.animating = False
            animation_controller.current_function = None

            transform_manager.addTransformations(
                x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
            )

            # enqueue all transformations
            while not transform_manager.transformations_queue.isEmpty():
                transformation = transform_manager.transformations_queue.dequeue()
                animation_controller.enqueueAnimation(transformation)

            print("Transformations queued for animation")


        if differentiate_button.isClicked(event) and function_entered:
            transform_manager.addDifferentiation()

            # clear old animations
            animation_controller.queue.clear()
            animation_controller.animating = False
            animation_controller.current_function = None

            # enqueue the differentiation
            while not transform_manager.transformations_queue.isEmpty():
                transformation = transform_manager.transformations_queue.dequeue()
                animation_controller.enqueueAnimation(transformation)

            print("Differentiation queued for animation")

        if transformation_tab_button.isClicked(event):
            current_tab = "transformations"

        if differentiation_tab_button.isClicked(event):
            current_tab = "differentiation"


    mouse_pos = pygame.mouse.get_pos()
    submit_func_button.update(mouse_pos)
    submit_trans_button.update(mouse_pos)
    transformation_tab_button.update(mouse_pos)
    differentiation_tab_button.update(mouse_pos)

    # Draw all UI elements
    
    function_text.draw(screen)
    y_text.draw(screen)
    function_box.draw(screen)
    submit_func_button.draw(screen)

    if current_tab == "transformations":
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

    if current_tab == "differentiation":
        differentiate_button.draw(screen)
    

    transformation_tab_button.draw(screen)
    differentiation_tab_button.draw(screen)

    # Draw arrow pointing at current transformation (skip differentiation)
    if animation_controller.animating and animation_controller.transformation.type != "differentiate":
        key = (animation_controller.transformation.type, animation_controller.transformation.axis)
        target_rect = transform_to_ui.get(key)
        if target_rect:
            # Position arrow to the right of the UI element
            arrow_pos = (target_rect.right + arrow_img.get_width() + 5, target_rect.centery - arrow_img.get_height() // 2)
            screen.blit(arrow_img, arrow_pos)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
