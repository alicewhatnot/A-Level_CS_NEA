import pygame
from core.ast import evaluateAST

class AnimationController:
    def __init__(self, graph_plotter, duration=1000):
        """
        graph_plotter: GraphPlotter instance
        duration: animation duration in ms
        """
        self.graph_plotter = graph_plotter
        self.duration = duration
        self.animating = False
        self.start_time = None
        self.prev_function = None
        self.next_function = None

    def startAnimation(self, prev_function, next_function):
        """Begin interpolating from prev_function to next_function."""
        self.prev_function = prev_function
        self.next_function = next_function
        self.start_time = pygame.time.get_ticks()
        self.animating = True

    def update(self, screen):
        """Update the animation each frame. Draw either morphing or static state."""
        if not self.animating:
            self.graph_plotter.drawAll(screen)
            return

        # time progress
        now = pygame.time.get_ticks()
        t = (now - self.start_time) / self.duration
        if t >= 1.0:
            # animation done
            self.graph_plotter.functions = [self.graph_plotter.functions[0], self.next_function]
            self.animating = False
            self.graph_plotter.drawAll(screen)
            return

        # interpolate between prev and next
        self.drawMorph(screen, t)

    def drawMorph(self, screen, t):
        """
        Interpolate between prev_function and next_function at progress t ∈ [0,1].
        """
        from settings import WIDTH, HEIGHT, SIDEBAR_WIDTH
        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        graph_height = HEIGHT
        center_x = graph_left + graph_width // 2
        center_y = graph_height // 2
        scale = 40

        prev_tree = self.prev_function.getFunction()
        next_tree = self.next_function.getFunction()
        colour = self.next_function.getColour()

        points = []
        for px in range(graph_left, WIDTH):
            x_val = (px - center_x) / scale

            y_prev = evaluateAST(prev_tree, x_val)
            y_next = evaluateAST(next_tree, x_val)
            if y_prev is None or y_next is None:
                continue

            # linear interpolation between old and new y values
            y_val = (1 - t) * y_prev + t * y_next
            py = center_y - int(y_val * scale)

            if 0 <= py <= HEIGHT:
                points.append((px, py))

        if len(points) > 1:
            pygame.draw.lines(screen, colour, False, points, 2)
