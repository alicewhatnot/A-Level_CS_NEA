import pygame
from collections import deque
from core.ast import copyAST
from core.function import Function
from core.modify_function import ShiftFunction, StretchFunction, ReflectFunction, DifferentiateFunction
import math


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

    def update(self, screen, dual_view=False):
        # No animation running
        if not self.animating:
            if self.current_function:
                # draw original (gray) + final transformed
                self.graph_plotter.drawFunction(
                    screen, self.graph_plotter.functions[0], color_override=(150, 150, 150)
                )
                self.graph_plotter.drawFunction(screen, self.current_function)
            else:
                self.graph_plotter.drawAll(screen, dual_view=dual_view)
            return

        # During animation
        now = pygame.time.get_ticks()
        t = (now - self.start_time) / self.duration
        t_clamped = max(0.0, min(t, 1.0))

        if t >= 1.0:
            # finalize this transform
            final_func = self._applyTransformation(self.base_function, self.transformation, 1.0)
            self.current_function = final_func

            if self.transformation.type != "differentiate":
                # store stable state AFTER finishing
                self.graph_plotter.functions = [self.graph_plotter.functions[0], final_func]

            # draw the final frame of this transform
            if self.transformation.type == "differentiate" or dual_view:
                self.graph_plotter.drawAll(screen, dual_view=True, derivative_function=final_func)
            else:
                self.graph_plotter.drawFunction(
                    screen, self.graph_plotter.functions[0], color_override=(150, 150, 150)
                )
                self.graph_plotter.drawFunction(screen, final_func)

            # prepare next transform and bail out this frame to avoid drawing a new intermediate now
            self._startNext()
            return  # <-- crucial to prevent the one-frame flash

        # Draw intermediate frame
        intermediate_func = self._applyTransformation(self.base_function, self.transformation, t_clamped)

        if self.transformation.type == "differentiate" or dual_view:
            self.graph_plotter.drawAll(screen, dual_view=True, derivative_function=intermediate_func)
        else:
            self.graph_plotter.drawFunction(
                screen, self.graph_plotter.functions[0], color_override=(150, 150, 150)
            )
            self.graph_plotter.drawFunction(screen, intermediate_func)


    def _applyTransformation(self, base_func, transformation, t):
        ast_copy = copyAST(base_func.getFunction())
        copy_variable = base_func.function_variable
        temp_func = Function(ast_copy, copy_variable)

        if transformation.type == "shift":
            interpolated_value = t * transformation.value
            modifier = ShiftFunction(temp_func, transformation.axis, interpolated_value)

        elif transformation.type == "stretch":
            interpolated_value = 1 + (transformation.value - 1) * t
            modifier = StretchFunction(temp_func, transformation.axis, interpolated_value)

        elif transformation.type == "reflect":
            ast_copy = copyAST(base_func.getFunction())
            copy_variable = base_func.function_variable
            temp_func = Function(ast_copy, copy_variable)

            # Nonlinear easing
            # t=0 → scale=1, t=1 → scale=-1
            eased_t = math.sin(t * math.pi / 2)  # smooth "ease-out"
            scale = (1 - 2 * eased_t)

            if transformation.axis == 'x':
                return StretchFunction(temp_func, 'y', scale).ModifyFunction()
            elif transformation.axis == 'y':
                return StretchFunction(temp_func, 'x', scale).ModifyFunction()


        elif transformation.type == "differentiate":
            modifier = DifferentiateFunction(temp_func)

        else:
            return temp_func

        return modifier.ModifyFunction()
