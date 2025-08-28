from core.function_entry import FunctionEntry
from core.graph_plotter import GraphPlotter
from core.function import Function 
from core.transform_manager import TransformManager 
from core.animation_controller import AnimationController
from core.ast import containsTrigFunction
from core.queue import Queue
import pygame
import sys

from settings import WIDTH, HEIGHT, SIDEBAR_WIDTH, FPS, MATHS_FONT, COLOUR_BACKGROUND, COLOUR_SIDEBAR, COLOUR_INACTIVE, COLOUR_FAIL
from ui_elements import InputBox, Checkbox, Button, Text
from graph_ui import drawGraphArea

pygame.init()
pygame.key.set_repeat(300, 50)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Function Transformation UI")
from settings import load_assets

# UI Elements & Assets

arrow_img, tick_img = load_assets()

function_text = Text(20,30, "Enter Function")
pre_text = Text(20,66, "f(x) =")
function_box = InputBox(75, 60, 250, 40, font=MATHS_FONT)

differentiate_button = Button(20, 120, 140, 32, "Differentiate")
reset_button = Button(170, 120, 140, 32, "Reset")

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

# Creating overseeing classes 
graph_plotter = GraphPlotter()
animation_controller = AnimationController(graph_plotter, duration=2000)  # 1s per transformation

# Defining flags & variables
function_entered = False
current_tab = "transformations"
previous_transformations = []
current_displayed_function = None
derivative_order = 0
dual_view = False

while running:
    # Background & sidebar drawn
    screen.fill(COLOUR_BACKGROUND)
    pygame.draw.rect(screen, COLOUR_SIDEBAR, (0, 0, SIDEBAR_WIDTH, HEIGHT))

    # Checking whether the graph should use degrees
    use_degrees = False
    if current_displayed_function and not dual_view:
        function_tree = current_displayed_function.getFunction()
        if containsTrigFunction(function_tree):
            use_degrees = True

    # Checking the variable to display on the axis
    if current_displayed_function:
        current_variable = current_displayed_function.getFunctionVar()
    else:
        current_variable = "x"

    # Drawing the graph
    if current_variable == None:
        drawGraphArea(screen, derivative_order, dual_view, use_degrees=use_degrees, variable="x")
    else:
        drawGraphArea(screen, derivative_order, dual_view, use_degrees=use_degrees, variable=current_variable)
        pre_text.setText(f"f({current_variable}) =")

    # Updating the animating controller to display a function once entered
    if function_entered:
        animation_controller.update(screen, dual_view)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Calling event handling for the user inputs
        function_box.handleEvent(event)

        x_stretch_box.handleEvent(event)
        y_stretch_box.handleEvent(event)
        x_shift_box.handleEvent(event)
        y_shift_box.handleEvent(event)
        x_reflect.handleEvent(event)
        y_reflect.handleEvent(event)

        # Submit function
        if (event.type == pygame.KEYDOWN and function_box.active):

            # Text recieved, passed to an object responsible for creating function objects from user input
            user_function_text = function_box.getText()
            user_function_entry = FunctionEntry(user_function_text) 

            # User input is parsed
            success = user_function_entry.parseFunction()

            if  success:
                # If successful parsing then convert to an AST
                user_function_entry.functionAST()

                function_tree, function_variable = user_function_entry.outputFunction()

                # Function object created
                function_object = Function(function_tree, function_variable)

                # Plotted and related flags updated
                graph_plotter.plotFunction(function_object)  
                function_entered = True
                current_displayed_function = function_object
                
                # Animation controller can now be updated and the transformation manager can be created
                animation_controller.current_function = function_object
                transform_manager = TransformManager(function_object)
                animation_controller.addTransformManager(transform_manager)

                # Clearing any animations or transformations from any previous valid inputs
                animation_controller.queue.clear()
                animation_controller.animating = False
                previous_transformations = None
                

            else:
                # Clearing any inputs to ensure the user sees nothing, an indication of an invalid entry
                graph_plotter.functions = []   
                function_entered = False
                current_displayed_function = None
                

        # Submit transformations
        if submit_trans_button.isClicked(event) and function_entered:

            # Clear the animation queue before adding
            animation_controller.queue.clear()
            animation_controller.animating = False
            animation_controller.current_function = None

            transform_manager.addTransformations(
                x_stretch_box, y_stretch_box, x_shift_box, y_shift_box, x_reflect, y_reflect
            )

            # Enqueue all transformations
            while not transform_manager.transformations_queue.isEmpty():
                transformation = transform_manager.transformations_queue.dequeue()
                animation_controller.enqueueAnimation(transformation)
            print("Transformations queued for animation")

        # Differentiate
        if differentiate_button.isClicked(event) and function_entered:
            # Special case of animation controller in which no animation occurs
            animation_controller.differentiate()

            # Then order increased to 1 for representation on the graph axis            
            derivative_order += 1
            print(f"Differentiation queued. Now at order {derivative_order}")

        # Reset differentiation
        if reset_button.isClicked(event) and function_entered:
            # Reset Derivative Order
            derivative_order = 0

            # Stop ongoing animations
            animation_controller.queue.clear()
            animation_controller.animating = False

            # Reset GraphPlotter to show only original function
            graph_plotter.plotFunction(current_displayed_function)

            # Reset AnimationController derivative state
            animation_controller.current_function = current_displayed_function
            animation_controller.top_function = None
            animation_controller.bottom_function = None
            animation_controller.differentiating = False
            animation_controller.transform_manager.setBaseFunction(current_displayed_function)

            print("Derivative cycle fully reset")

        # Allowing the user to change tabs between the two modes
        if transformation_tab_button.isClicked(event):
            current_tab = "transformations"

        if differentiation_tab_button.isClicked(event):
            current_tab = "differentiation"

    # Getting the mouse position and passing to buttons for a hover effect
    mouse_pos = pygame.mouse.get_pos()
    submit_trans_button.update(mouse_pos)
    transformation_tab_button.update(mouse_pos)
    differentiation_tab_button.update(mouse_pos)

    # Drawing UI elements
    function_text.draw(screen)
    pre_text.draw(screen)
    function_box.draw(screen)

    # Transformation specific
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
        dual_view = False

    # Differentiation specific
    if current_tab == "differentiation":
        differentiate_button.draw(screen)
        reset_button.draw(screen)
        dual_view = True
    
    # Tabs
    transformation_tab_button.draw(screen)
    differentiation_tab_button.draw(screen)

    # Draw arrow pointing at current transformation 
    if animation_controller.animating and animation_controller.transformation.type != "differentiate":
        key = (animation_controller.transformation.type, animation_controller.transformation.axis)
        target_rect = transform_to_ui.get(key)
        if target_rect:
            # Positioning
            arrow_pos = (target_rect.right + arrow_img.get_width() + 5, target_rect.centery - arrow_img.get_height() // 2)
            screen.blit(arrow_img, arrow_pos)


    pygame.display.flip()
    # Main loop repeats FPS times per second
    clock.tick(FPS)

pygame.quit()
sys.exit()
