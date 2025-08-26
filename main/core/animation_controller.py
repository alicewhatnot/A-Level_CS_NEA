import pygame
from collections import deque
from core.ast import copyAST
from core.function import Function
from core.modify_function import ShiftFunction, StretchFunction, ReflectFunction, DifferentiateFunction
import math


class AnimationController:
    def __init__(self, graph_plotter, duration=1000, gap=500):
        self.graph_plotter = graph_plotter
        self.duration = duration
        self.gap = gap                  # gap in ms
        self.queue = deque()
        self.animating = False
        self.start_time = None
        self.base_function = None
        self.transformation = None
        self.current_function = None
        self.in_gap = False              # new state for pause
        self.gap_start_time = None


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
        if self.in_gap:
            now = pygame.time.get_ticks()
            # Keep drawing the finished function throughout the gap
            self.graph_plotter.drawFunction(
                screen, self.graph_plotter.functions[0], color_override=(150,150,150)
            )
            self.graph_plotter.drawFunction(screen, self.current_function)

            if now - self.gap_start_time >= self.gap:
                self.in_gap = False
                self._startNext()   # proceed to next animation
            return


        # No animation running
        if not self.animating:
            if self.current_function:
                if dual_view:
                    # Differentiation: top = original, bottom = derivative
                    self.graph_plotter.drawAll(screen, dual_view=True, derivative_function=self.current_function)
                else:
                    # Single graph: gray old + last transformed function
                    self.graph_plotter.drawFunction(
                        screen, self.graph_plotter.functions[0], color_override=(150,150,150)
                    )
                    self.graph_plotter.drawFunction(screen, self.current_function)
            else:
                # Nothing yet, just draw whatever functions exist
                self.graph_plotter.drawAll(screen, dual_view=dual_view)
            return

        now = pygame.time.get_ticks()
        t = (now - self.start_time) / self.duration
        t_clamped = max(0.0, min(t, 1.0))

       # In AnimationController.update
        if self.transformation.type == "differentiate":
            if self.current_function is None:
                # Compute derivative once
                self.current_function = self._applyTransformation(self.base_function, self.transformation, 1.0)

            # Progress of animation (0 → 1)
            progress = min(1.0, (now - self.start_time) / self.duration)

            if dual_view:
                self.graph_plotter.drawAll(
                    screen,
                    dual_view=True,
                    derivative_function=self.current_function  # pass Function object only
                )

            else:
                # Single graph: gray original + traced derivative
                self.graph_plotter.drawFunction(
                    screen, self.graph_plotter.functions[0], color_override=(150,150,150)
                )
                self.graph_plotter.drawFunction(screen, self.current_function, progress=progress)

            if progress >= 1.0:
                self._startNext()
            return


        # Normal animation for shift/stretch/reflect
        intermediate_func = self._applyTransformation(self.base_function, self.transformation, t_clamped)

        if t >= 1.0:
            # Finish this transformation
            self.current_function = intermediate_func

            # Start gap immediately
            self.in_gap = True
            self.gap_start_time = pygame.time.get_ticks()

            # Draw the final frame for the first tick of the gap
            self.graph_plotter.drawFunction(
                screen, self.graph_plotter.functions[0], color_override=(150,150,150)
            )
            self.graph_plotter.drawFunction(screen, self.current_function)
            return


        # Draw intermediate frame: gray original + intermediate function
        self.graph_plotter.drawFunction(screen, self.graph_plotter.functions[0], color_override=(150,150,150))
        self.graph_plotter.drawFunction(screen, intermediate_func)



    def _applyTransformation(self, base_func, transformation, t):
        # Make a copy of the AST and function object
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
            # Nonlinear easing for visual effect
            eased_t = math.sin(t * math.pi / 2)
            scale = (1 - 2 * eased_t)

            if transformation.axis == 'x':
                return StretchFunction(temp_func, 'y', scale).ModifyFunction()
            elif transformation.axis == 'y':
                return StretchFunction(temp_func, 'x', scale).ModifyFunction()

        elif transformation.type == "differentiate":
            # Differentiation: return derivative immediately, no animation
            return DifferentiateFunction(temp_func).ModifyFunction()

        else:
            # Unknown transformation: return function as-is
            return temp_func

        # Apply modifier for shift/stretch
        return modifier.ModifyFunction()
