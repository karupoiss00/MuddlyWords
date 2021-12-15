""" File with some objects for easier debugging of game """

from weakref import ref

import pygame
from psutil import Process, cpu_count

from .hitbox import Hitbox, Ellipse


class DebugModule:
    """Debug module - part of Debugger. Every debug module must have at least three
    functions: `__init__`, `interval_update`, `static_update`. I could have written
    all the modules directly in the Debugger, but I didn't do this to get rid of the
    confusion in the code and to modify them more easily, so each module should
    perform a specific task
    """

    def __init__(self, *args, **kwargs) -> None:
        """Function is called only once when the module is enabled. Here the module gets
        and saves certain objects for further use and performs the configuration itself
        """
        pass

    def interval_update(self) -> None:
        """Function is called after a certain time interval,
        which defined in the Debugger
        """
        pass

    def static_update(self) -> None:
        """Function is called on each iteration of game loop
        """
        pass


class DebugStat(DebugModule):
    """Debug module for viewing the current state of CPU usage, RAM,
    and other game and system information in the lower-left corner
    """

    # Color of information text
    COLOR = (158, 46, 255)

    def __init__(self, screen, base_dir, clock) -> None:
        """Initializes the module, saving objects and configuring itself

        Args:
            screen (pygame.Surface): Screen (surface) obtained via pygame
            base_dir (str): An absolute path to directory where file with the main
                entrypoint is located
            clock (pygame.time.Clock): Clock object obtained via pygame
        """
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.process = Process()

        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 25)

        self.clock = clock

    def interval_update(self) -> None:
        """In current module, this function is used to update the text
        of the debugging information
        """
        # Creating list of messages as plain text
        self.msgs = (
            f'FPS: {round(self.clock.get_fps(), 5)}',
            f'POS: {str(pygame.mouse.get_pos())}',
            f'RAM: {round(self.process.memory_info().rss / 1024 / 1024, 3)} MB',
            f'CPU: {round(self.process.cpu_percent() / cpu_count(), 2)}%'
        )

        # Defining lists of images and rectangles for using in future
        self.imgs = []
        self.rects = []

        # Vertical placing of the first row (bottom)
        y = self.screen_rect.bottom - 2

        for msg in self.msgs:
            # Generating image and rect for each message
            img = self.font.render(msg, True, self.COLOR)
            rect = img.get_rect()

            # Placing of rect (bottom-left)
            rect.right = self.screen_rect.right - 3
            rect.bottom = y

            # Adding image and rect to lists for blitting them in future
            self.imgs.append(img)
            self.rects.append(rect)

            # Reducing the margin from the top of screen, which means
            # that messages will be drawn from the bottom up
            y -= 17

    def static_update(self) -> None:
        """In current module, this function is used for
        blitting information messages
        """
        # Blitting debug information messages
        for i in range(len(self.msgs)):
            self.screen.blit(self.imgs[i], self.rects[i])


class DebugHitbox(DebugModule):
    """Debug module for drawing hitbox of every image
    """

    # Color of hitbox
    COLOR_RECT = (0, 255, 0)
    COLOR_ELLIPSE = (0, 255, 255)

    def __init__(self, screen) -> None:
        """Initializes the module. Replaces the default `__init__`
        function of `Hitbox` to track its instances

        Args:
            screen (pygame.Surface): Screen (surface) obtained via pygame
        """

        # Saving screen for the further use
        self.screen = screen

        # Creating list of hiboxes
        self.hitboxes = []

        # Saving original `__init__` and list of hitboxes
        globals()['origin_hitbox_init'] = Hitbox.__init__
        globals()['hitboxes'] = self.hitboxes

        # Replacing default `__init__` function with custom function
        Hitbox.__init__ = self.__hitbox_init

    @staticmethod
    def __hitbox_init(self, *args, **kwargs):
        """Initializing :hitbox:`spaceway.hitbox.Hitbox` with default method
        and adding hitbox to list to track its
        """
        # Adding hitbox to list
        hitboxes.append(ref(self, hitboxes.remove))

        # Calling original `__init__` function
        return origin_hitbox_init(self, *args, **kwargs)

    def static_update(self):
        """Blitting all hitboxes on a given surface (screen)
        """
        for hitbox in self.hitboxes:
            if isinstance(hitbox(), Ellipse):
                pygame.draw.ellipse(self.screen, self.COLOR_ELLIPSE, hitbox(), 1)
            else:
                pygame.draw.rect(self.screen, self.COLOR_RECT, hitbox(), 1)


class Debugger:
    """Debugger class, manages debug modules
    """

    # Interval for calling `interval_update` of modules (in seconds)
    UPDATE_INTERVAL = 0.5

    def __init__(self, FPS) -> None:
        """Initializing of Debugger, configuring itself

        Args:
            FPS (int): The FPS of the game is defined in the configuration
        """
        # Setting objects for further using
        self.__modules = []
        self.__tick = 0
        self.__FPS = FPS

    def enable_module(self, module, *args, **kwargs) -> None:
        """Enables a debug module

        Args:
            module (spaceway.debug.DebugModule): Module object which should
                be initialized
            *args (any): Arguments needed to initialize the module
            **kwargs (any): Keyword arguments needed to initialize the module
        """
        self.__modules.append(module(*args, **kwargs))

    def update(self) -> None:
        """Updates debug modules
        """
        # If `tick` overflow, reset it
        if self.__tick == 10 * self.__FPS:
            self.__tick = 0

        for module in self.__modules:
            # Calling `interval_update` if the time has come
            if self.__tick % (self.UPDATE_INTERVAL * self.__FPS) == 0:
                module.interval_update()

            # Calling `static_update`
            module.static_update()

        # Tick increase
        self.__tick += 1
