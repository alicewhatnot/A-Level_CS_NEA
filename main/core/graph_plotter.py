import pygame
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

    def drawAll(self, screen):
        """Draw all stored functions every frame."""
        for function in self.functions:
            self.drawFunction(screen, function)

    def drawFunction(self, screen, function_object, color_override=None):
        """
        Draw a function on the screen.
        
        color_override: if provided, uses this color instead of function_object's color
        """
        function_tree = function_object.getFunction()
        colour = color_override or function_object.getColour()  # use override if given

        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        graph_height = HEIGHT
        center_x = graph_left + graph_width // 2
        center_y = graph_height // 2

        scale = 40
        points = []

        for px in range(graph_left, WIDTH):
            x_val = (px - center_x) / scale
            y_val = evaluateAST(function_tree, x_val)
            if y_val is None:
                continue
            py = center_y - int(y_val * scale)
            if 0 <= py <= HEIGHT:
                points.append((px, py))

        if len(points) > 1:
            pygame.draw.lines(screen, colour, False, points, 2)
