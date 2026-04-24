import pygame
from core.ast import copyAST
from core.ast import containsTrigFunction
from core.function import Function
from core.modify_function import DifferentiateFunction
from core.queue import Queue

class AnimationController:
    def __init__(self, graph_plotter, duration=1000, gap=500):
        self.graph_plotter = graph_plotter
        self.duration = duration
        self.gap = gap                  
        self.queue = Queue(6)
        self.animating = False
        self.start_time = None
        self.base_function = None
        self.transformation = None
        self.current_function = None
        self.in_gap = False              
        self.gap_start_time = None
        self.transform_manager = None
        self.top_function = None
        self.bottom_function = None
        self.differentiating = False
        self.use_degrees =  True      
        self.paused = False
        self.pending_pause = False

    def setUseDegrees(self, flag):
            self.use_degrees = flag

    def addTransformManager(self, transform_manager):
        """
        Add the transformation manager
        This is a method not part of the constructor as the controller is created before the transformation manager
        """
        self.transform_manager = transform_manager

    def enqueueAnimation(self, transformation):
        """
        Queues a transformation animation
        """
        self.queue.enqueue(transformation)

        # If nothing is animating, start animation immediatly
        if not self.animating:
            self.startNext()

    def startNext(self):
        """
        Animates the first transformation in the queue
        """
        if self.queue.isEmpty():
            self.animating = False
            return

        # Fetch the transformation and function for animation
        self.transformation = self.queue.dequeue()
        self.base_function = self.current_function or self.graph_plotter.getBaseFunction()

        # Start animating and timing
        self.start_time = pygame.time.get_ticks()
        self.animating = True


    def update(self, screen, dual_view=False):
        """
        Updates and renders the current animation state        
        """
        # Determine top and bottom functions for dual view (if present)
        top_func = self.top_function or self.current_function
        bottom_func = self.bottom_function if self.differentiating else None

        # Dual view mode
        if dual_view:
            self.graph_plotter.drawAll(
                screen,
                dual_view=True,
                top_function=top_func,
                bottom_function=bottom_func,
                use_degrees=self.use_degrees
            )

            # If differentiating don't draw
            if self.differentiating:
                return

        # Gap between animations
        if self.in_gap:
            now = pygame.time.get_ticks()

            # Draw original and current function
            self.graph_plotter.drawFunction(screen, self.graph_plotter.getBaseFunction(),
                                            colour_override=(150,150,150), use_degrees=self.use_degrees)
            self.graph_plotter.drawFunction(screen, self.current_function, use_degrees=self.use_degrees)

            # Don't leave gap if paused
            if self.paused:
                return 

            # If pending pause when leaving gap then don't leave
            if now - self.gap_start_time >= self.gap:
                if self.pending_pause:
                    self.pending_pause = False
                    self.paused = True
                else:
                    # Otherwise leave
                    self.in_gap = False
                    self.startNext()
            return


        # No animation running
        if not self.animating:
            if self.current_function:
                if dual_view:
                    # Draw top as base function, bottom as derivative if exists
                    self.graph_plotter.drawAll(screen, dual_view=True, top_function=top_func, bottom_function=bottom_func, use_degrees=self.use_degrees)
                else:
                    # Draw gray old function and the current transformed function
                    self.graph_plotter.drawFunction(screen, self.graph_plotter.getBaseFunction(), colour_override=(150,150,150), use_degrees=self.use_degrees)
                    self.graph_plotter.drawFunction(screen, self.current_function, use_degrees=self.use_degrees)
            else:
                # If no function then draw whatever is in graph plotter
                self.graph_plotter.drawAll(screen, dual_view=dual_view, use_degrees=self.use_degrees)
            return

        # Calculates how far along the animation is
        now = pygame.time.get_ticks()
        progress = (now - self.start_time) / self.duration
        # Make sure the progress doesn't leave 0-1
        progress_safe = max(0.0, min(progress, 1.0))

        if (self.use_degrees 
            and self.transformation.getType() == "shift" 
            and self.transformation.getAxis() == 'x'
            and containsTrigFunction(self.base_function.getFunction())):
            self.transformation.convertToRad()
            
        # Animates shifts stretches and reflections 
        intermediate_function = self.transform_manager.applyTransformation(
            self.transformation,
            progress_safe,
            base_function=self.base_function
        )

        if progress >= 1.0:
            # Finish this transformation
            self.current_function = self.transform_manager.applyTransformation(
                self.transformation,
                1.0,
                base_function=self.base_function
            )

            # Start gap 
            self.in_gap = True
            self.gap_start_time = pygame.time.get_ticks()

            # Draw the final frame for the first tick of the gap
            self.graph_plotter.drawFunction(
                screen, self.graph_plotter.getBaseFunction(), colour_override=(150,150,150), use_degrees=self.use_degrees
            )
            self.graph_plotter.drawFunction(screen, self.current_function, use_degrees=self.use_degrees)
            return

        # Draw intermediate frame of gray original and intermediate animated function
        self.graph_plotter.drawFunction(screen, self.graph_plotter.getBaseFunction(), colour_override=(150,150,150), use_degrees=self.use_degrees)
        self.graph_plotter.drawFunction(screen, intermediate_function, use_degrees=self.use_degrees)

    # Specific method for differentiating
    def differentiate(self):
        if not self.transform_manager:
            return False

        # Make a copy of the current function to use on the top graph
        previous_derivative = Function(
            copyAST(self.transform_manager.getCurrentFunction().getFunction()),
            self.transform_manager.getCurrentFunction().getFunctionVar(),
            self.transform_manager.getCurrentFunction().getColour(),
        )

        # Create the new derivative from the previous copy
        new_derivative = DifferentiateFunction(
            Function(copyAST(previous_derivative.getFunction()), previous_derivative.getFunctionVar(), previous_derivative.getColour())
        ).ModifyFunction()

        if new_derivative == None:
            return False
        
        # Update the transform manager
        self.transform_manager.setBaseFunction(new_derivative)

        print("Top:", previous_derivative.getFunction())
        print("Bottom:", new_derivative.getFunction())

        # Update attributes to be accessed by the update method
        self.top_function = previous_derivative
        self.bottom_function = new_derivative
        self.differentiating = True

        return True
    
    def togglePause(self):
        """Pause or resume animation in a safe way."""
        if self.paused or self.pending_pause:
            self.paused = False
            self.pending_pause = False
        else:
            if self.animating:
                self.pending_pause = True
            elif self.in_gap:
                self.paused = True

    def forceResume(self):
        """
        Resume from pause if any, for use when wiping animation
        """
        self.paused = False
        self.pending_pause = False