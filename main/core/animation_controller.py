import pygame
from collections import deque
from core.ast import copyAST
from core.function import Function
from core.modify_function import ShiftFunction, StretchFunction, ReflectFunction


class AnimationController:
    def __init__(self, graph_plotter, duration=1000):
        """
        graph_plotter: GraphPlotter instance
        duration: ms per transformation animation
        """
        self.graph_plotter = graph_plotter
        self.duration = duration
        self.queue = deque()
        self.animating = False
        self.start_time = None
        self.base_function = None
        self.transformation = None
        self.current_function = None
        self.original_color_override = None

    def enqueueAnimation(self, transformation):
        """Queue a transformation animation."""
        self.queue.append(transformation)

        # if nothing is animating, start right away
        if not self.animating:
            self._startNext()

    def _startNext(self):
        if not self.queue:
            self.animating = False
            return

        self.transformation = self.queue.popleft()
        self.base_function = self.current_function or self.graph_plotter.functions[0]
        self.start_time = pygame.time.get_ticks()
        self.animating = True

    def update(self, screen):
        if not self.animating:
            # If no animation running, draw original + last transformed
            if self.current_function:
                # Original function stays grey once any animation has occurred
                self.graph_plotter.drawFunction(
                    screen, self.graph_plotter.functions[0],
                    color_override=self.original_color_override or (150, 150, 150)
                )
                self.graph_plotter.drawFunction(screen, self.current_function)
            else:
                self.graph_plotter.drawAll(screen)
            return

        now = pygame.time.get_ticks()
        t = (now - self.start_time) / self.duration

        if t >= 1.0:
            # Finish: apply full transformation
            final_func = self._applyTransformation(self.base_function, self.transformation, 1.0)
            self.current_function = final_func
            self.graph_plotter.functions = [self.graph_plotter.functions[0], final_func]

            # Set original color override so it stays grey permanently
            self.original_color_override = (150, 150, 150)

            self._startNext()

        # During animation: original grey, transforming function solid
        intermediate_func = self._applyTransformation(self.base_function, self.transformation, min(t, 1.0))
        self.graph_plotter.functions = [self.graph_plotter.functions[0], intermediate_func]

        self.graph_plotter.drawFunction(
            screen, self.graph_plotter.functions[0],
            color_override=self.original_color_override or (150, 150, 150)
        )
        self.graph_plotter.drawFunction(screen, intermediate_func)

    def _applyTransformation(self, base_func, transformation, t):
        """Return a Function object with transformation interpolated by t ∈ [0,1]."""
        ast_copy = copyAST(base_func.getFunction())
        temp_func = Function(ast_copy)

        if transformation.type == "shift":
            interpolated_value = t * transformation.value
            modifier = ShiftFunction(temp_func, transformation.axis, interpolated_value)

        elif transformation.type == "stretch":
            interpolated_value = 1 + (transformation.value - 1) * t
            modifier = StretchFunction(temp_func, transformation.axis, interpolated_value)

        elif transformation.type == "reflect":
            if t < 0.5:
                return temp_func  # no reflect yet
            modifier = ReflectFunction(temp_func, transformation.axis)

        else:
            return temp_func

        return modifier.ModifyFunction()
