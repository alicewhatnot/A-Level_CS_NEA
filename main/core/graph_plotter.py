import pygame
import math
from settings import WIDTH, HEIGHT
from core.ast import evaluateAST   
from settings import SIDEBAR_WIDTH

def draw_thick_aaline(screen, colour, points, thickness=4):
    """Draw a thick anti-aliased line, automatically clipping points off-screen."""
    if len(points) < 2:
        return

    offsets = []
    half = thickness // 2
    for dx in range(-half, half + 1):
        for dy in range(-half, half + 1):
            offsets.append((dx, dy))

    for dx, dy in offsets:
        offset_points = [(x + dx, y + dy) for x, y in points]

        # Pygame automatically clips lines that go off-screen
        for i in range(1, len(offset_points)):
            pygame.draw.aaline(screen, colour, offset_points[i-1], offset_points[i])


class GraphPlotter:
    def __init__(self):
        self.functions = [] 
        self.dual_view = False

    def plotFunction(self, function_object):
        """Clears old graph and plots only the new user function."""
        self.functions = [function_object]

    def plotSubsequent(self, function_object):
        """Adds a new transformed function without clearing."""
        self.functions.append(function_object)

    def drawAll(self, screen, dual_view=False, top_function=None, bottom_function=None):
        """
        Draws either a single graph or a dual-view graph.
        
        dual_view: if True, splits screen vertically.
        top_function: function to draw in the top half (previous derivative)
        bottom_function: function to draw in the bottom half (current derivative)
        """
        if not dual_view:
            # Normal mode: single graph
            for function in self.functions:
                self.drawFunction(screen, function)
        else:
            graph_height = HEIGHT // 2  # half height for each plot

            # --- Top graph ---
            if top_function:
                self.drawFunction(
                    screen, top_function,
                    y_offset=0, graph_height=graph_height,
                    
                )

            # --- Bottom graph ---
            if bottom_function:
                self.drawFunction(
                    screen, bottom_function,
                    y_offset=graph_height, graph_height=graph_height,
                )

    def drawFunction(self, screen, function_object, color_override=None, y_offset=0, graph_height=None):
        if graph_height is None:
            graph_height = HEIGHT 

        function_tree = function_object.getFunction()
        if function_tree is None:
            return
        variable = function_object.getFunctionVar()
        colour = color_override or function_object.getColour()

        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        center_x = graph_left + graph_width // 2
        center_y = y_offset + graph_height // 2
        scale = 40

        prev_py = None
        segment = []

        min_y = y_offset
        max_y = y_offset + graph_height - 5

        for px in range(graph_left, WIDTH):
            x_val = (px - center_x) / scale
            y_val = evaluateAST(function_tree, x_val, variable)

            if y_val is None or math.isnan(y_val) or math.isinf(y_val):
                # Discontinuity: draw current segment and reset
                if len(segment) > 1:
                    draw_thick_aaline(screen, colour, segment, thickness=3)
                segment = []
                prev_py = None
                continue

            py = center_y - int(y_val * scale)

            # Only append points inside bounds
            if min_y <= py <= max_y:
                # Break segment if jump is too large (vertical asymptote)
                if prev_py is not None and abs(py - prev_py) > graph_height / 2:
                    if len(segment) > 1:
                        draw_thick_aaline(screen, colour, segment, thickness=3)
                    segment = []

                segment.append((px, py))
                prev_py = py
            else:
                # Point out of bounds: draw segment so far and reset
                if len(segment) > 1:
                    draw_thick_aaline(screen, colour, segment, thickness=3)
                segment = []
                prev_py = None

        if len(segment) > 1:
            draw_thick_aaline(screen, colour, segment, thickness=3)
