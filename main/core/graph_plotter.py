import pygame
import math
from settings import WIDTH, HEIGHT
from core.ast import evaluateAST   
from settings import SIDEBAR_WIDTH

class GraphPlotter:
    def __init__(self):
        self.functions = [] 

    def plotFunction(self, function_object):
        """Clears old graph and plots only the new user function."""
        self.functions = [function_object]   

    def plotSubsequent(self, function_object):
        """Adds a new transformed function without clearing."""
        self.functions.append(function_object)

    def drawAll(self, screen, dual_view=False, derivative_function=None):
        if not dual_view:
            # Normal mode: single graph
            for function in self.functions:
                self.drawFunction(screen, function)
        else:
            # Dual view: split vertically
            graph_left = SIDEBAR_WIDTH
            graph_width = WIDTH - SIDEBAR_WIDTH
            graph_height = HEIGHT // 2  # half height for each plot
            center_x = graph_left + graph_width // 2

            # --- Top: Original function ---
            for function in self.functions:
                self.drawFunction(
                    screen, function,
                    y_offset=0, graph_height=graph_height
                )

            # --- Bottom: Derivative function ---
            if derivative_function:
                self.drawFunction(
                    screen, derivative_function,
                    y_offset=graph_height, graph_height=graph_height
                )

    def drawFunction(self, screen, function_object, color_override=None, y_offset=0, graph_height=None):
        if graph_height is None:
            graph_height = HEIGHT

        # Get AST and variable once
        output = function_object.outputFunction()
        if output is None:
            return
        function_tree, variable = output

        colour = color_override or function_object.getColour()

        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        center_x = graph_left + graph_width // 2
        center_y = y_offset + graph_height // 2 

        scale = 40
        points = []
        prev_py = None

        for px in range(graph_left, WIDTH):
            x_val = (px - center_x) / scale
            y_val = evaluateAST(function_tree, x_val, variable)
            if y_val is None or math.isnan(y_val) or math.isinf(y_val):
                prev_py = None
                continue

            py = center_y - int(y_val * scale)

            # Dynamic threshold: break if y jumps more than half the graph height
            if prev_py is not None and abs(py - prev_py) > graph_height / 2:
                prev_py = None  # break the line
                continue

            points.append((px, py))
            prev_py = py

        # Draw separate segments to avoid lines over asymptotes
        if points:
            segment = [points[0]]
            for i in range(1, len(points)):
                if abs(points[i][1] - points[i-1][1]) > graph_height / 2:
                    if len(segment) > 1:
                        pygame.draw.lines(screen, colour, False, segment, 2)
                    segment = [points[i]]
                else:
                    segment.append(points[i])
            if len(segment) > 1:
                pygame.draw.lines(screen, colour, False, segment, 2)
