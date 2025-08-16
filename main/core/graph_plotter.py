import pygame
from settings import WIDTH, HEIGHT
from core.ast import evaluateAST   
from settings import SIDEBAR_WIDTH

class GraphPlotter:
    def __init__(self):
        self.current_graph = None  

    def plotExpression(self, screen, expression_object):
        """Plots the initial expression (replaces current graph)."""
        self.current_graph = expression_object
        self._draw_expression(screen, expression_object)

    def plotSubsequent(self, screen, expression_object):
        """Plots additional expressions (like transformations) without clearing."""
        self._draw_expression(screen, expression_object)

    def _draw_expression(self, screen, expression_object):
        expression_tree = expression_object.getExpression()
        colour = expression_object.getColour()

        # Graph area
        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        graph_height = HEIGHT
        center_x = graph_left + graph_width // 2
        center_y = graph_height // 2

        points = []
        # loop over screen x-coords
        for px in range(graph_left, WIDTH):  
            # Convert screen x to mathematical x 
            scale = 40
            x_val = (px - center_x) / scale

            y_val = evaluateAST(expression_tree, x_val) 
            if y_val is None:
                continue

            # Convert mathematical y to screen y
            py = center_y - int(y_val * scale)

            if 0 <= py <= HEIGHT:
                points.append((px, py))

        if len(points) > 1:
            pygame.draw.lines(screen, colour, False, points, 2)
