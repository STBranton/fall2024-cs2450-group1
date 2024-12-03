"""
Input handler module
"""
import asyncio
from abc import ABC, abstractmethod

from kivy.clock import Clock


class InputHandler(ABC):
    """
    Abstract base class for handling input in different environments.

    Subclasses must implement the `get_input` method to handle input asynchronously.
    """
    @abstractmethod
    async def get_input(self):
        """
        Asynchronously retrieves input from the user.

        Returns:
            str: The input provided by the user.
        """

class CLIInputHandler(InputHandler):
    """
    Handles input from the command-line interface (CLI) asynchronously.
    """
    async def get_input(self):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, "Enter input: ")


class GUIInputHandler(InputHandler):
    """
        Handles input from a graphical user interface (GUI) asynchronously.

        This class interacts with a GUI instance to prompt the user for input
        and waits for the input to be provided via the GUI.
    """
    def __init__(self, gui_instance):

        self.gui = gui_instance
        self.loop = asyncio.get_event_loop()
        self.input_future = None

    async def get_input(self):
        """
        Prompts the user for input through the GUI and waits for the input to be provided.

        Returns:
            str: The input provided by the user.

        This method uses an asyncio future to wait for the input, which is set by the GUI
        when the user provides input.
        """
        self.input_future = self.loop.create_future()
        # Schedule the GUI to prompt for input
        Clock.schedule_once(lambda dt: self.gui.enable_console_input(), 0)
        return await self.input_future

    def provide_input(self, value):
        """
        Sets the provided input as the result of the future and clears it.

        Args:
            value (str): The input provided by the user.
        """
        if self.input_future and not self.input_future.done():
            self.input_future.set_result(value)
            self.input_future = None
