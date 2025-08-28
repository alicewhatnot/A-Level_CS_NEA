import pygame
from collections import deque
from core.ast import copyAST, containsTrigFunction
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
        self.transform_manager = None
        self.top_function = None
        self.bottom_function = None
        self.differentiating = False


    def addTransformManager(self, transform_manager):
        self.transform_manager = transform_manager

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

        # Precompute derivative if needed
        if self.transformation.type == "differentiate":
            self.target_function = DifferentiateFunction(
                Function(copyAST(self.base_function.getFunction()), self.base_function.function_variable)
            ).ModifyFunction()
        else:
            self.target_function = None

        self.start_time = pygame.time.get_ticks()
        self.animating = True


    def update(self, screen, dual_view=False):
        # Determine top and bottom functions for dual view
        top_func = self.top_function or self.current_function
        bottom_func = self.bottom_function if self.differentiating else None

        # Dual view mode
        if dual_view:
            self.graph_plotter.drawAll(
                screen,
                dual_view=True,
                top_function=top_func,
                bottom_function=bottom_func
            )

            # If differentiating, skip further drawing
            if self.differentiating:
                return

        if self.in_gap:
            now = pygame.time.get_ticks()
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
                    # Draw top = base function, bottom = derivative if exists
                    self.graph_plotter.drawAll(screen, dual_view=True, top_function=top_func, bottom_function=bottom_func)
                else:
                    # Single graph: gray old + last transformed function
                    self.graph_plotter.drawFunction(screen, self.graph_plotter.functions[0], color_override=(150,150,150))
                    self.graph_plotter.drawFunction(screen, self.current_function)
            else:
                # Nothing yet, just draw whatever functions exist
                self.graph_plotter.drawAll(screen, dual_view=dual_view)
            return

        now = pygame.time.get_ticks()
        t = (now - self.start_time) / self.duration
        t_clamped = max(0.0, min(t, 1.0))

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

    def _applyTransformation(self, base_function, transformation, t):
        convert_degrees = containsTrigFunction(base_function.getFunction())

        # Compute interpolated value
        if transformation.type == "shift":
            if transformation.axis == "x" and convert_degrees:
                interpolated_value = t * transformation.value
            else:
                interpolated_value = t * transformation.value
            modifier = ShiftFunction(Function(copyAST(base_function.getFunction()), base_function.function_variable),transformation.axis, interpolated_value)

        elif transformation.type == "stretch":
            if transformation.axis == "x" and convert_degrees:
                interpolated_value = 1 + (transformation.value - 1) * t
            else:
                interpolated_value = 1 + (transformation.value - 1) * t
            modifier = StretchFunction(Function(copyAST(base_function.getFunction()), base_function.function_variable),
                transformation.axis, interpolated_value)

        elif transformation.type == "reflect":
            # Nonlinear easing for visual effect
            eased_t = math.sin(t * math.pi / 2)
            scale = (1 - 2 * eased_t)
            temp_func = Function(copyAST(base_function.getFunction()), base_function.function_variable)

            if transformation.axis == 'x':
                return StretchFunction(temp_func, 'y', scale).ModifyFunction()
            elif transformation.axis == 'y':
                return StretchFunction(temp_func, 'x', scale).ModifyFunction()

        elif transformation.type == "differentiate":
            temp_func = Function(copyAST(base_function.getFunction()), base_function.function_variable)
            return DifferentiateFunction(temp_func).ModifyFunction()

        else:
            return Function(copyAST(base_function.getFunction()), base_function.function_variable)

        # Apply modifier
        return modifier.ModifyFunction()

    def differentiate(self):
        if not self.transform_manager:
            return

        # Make a deep copy of the current function to use as top (previous)
        previous_derivative = Function(
            copyAST(self.transform_manager.current_function.getFunction()),
            self.transform_manager.current_function.getFunctionVar()
        )

        # Compute new derivative from a **fresh copy of previous_derivative**
        new_derivative = DifferentiateFunction(
            Function(copyAST(previous_derivative.getFunction()), previous_derivative.getFunctionVar())
        ).ModifyFunction()

        # Update transform manager
        self.transform_manager.setBaseFunction(new_derivative)

        print("Top:", previous_derivative.getFunction())
        print("Bottom:", new_derivative.getFunction())

        self.top_function = previous_derivative
        self.bottom_function = new_derivative
        self.differentiating = True
