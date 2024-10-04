import asyncio
from abc import ABC, abstractmethod
from kivy.clock import Clock

class InputHandler(ABC):
    @abstractmethod
    async def get_input(self):
        pass


class CLIInputHandler(InputHandler):
    async def get_input(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "Enter input: ")


class GUIInputHandler(InputHandler):
    def __init__(self, gui_instance):
        """
        Initialize with a reference to the GUI to enable input prompts.
        """
        self.gui = gui_instance
        self.loop = asyncio.get_event_loop()
        self.input_future = None

    async def get_input(self):
        self.input_future = self.loop.create_future()
        # Schedule the GUI to prompt for input
        Clock.schedule_once(lambda dt: self.gui.enable_console_input(), 0)
        return await self.input_future

    def provide_input(self, value):
        """
        Called by the GUI when input is provided by the user.
        """
        if self.input_future and not self.input_future.done():
            self.input_future.set_result(value)
            self.input_future = None
