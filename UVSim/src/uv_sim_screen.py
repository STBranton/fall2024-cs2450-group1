# uv_sim_screen.py

import asyncio
import os
import re

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from cpu import CPU
from input_handler import GUIInputHandler
from memory import Memory

# Define your theme colors
theme = [
    [76/255, 114/255, 29/255, 1],  # Dark green
    [1, 1, 1, 1],                  # White
]

class UVSimScreen(Screen):
    """
    Represents a screen in the UVSim application.

    This screen provides a GUI for interacting with the UVSim simulator, including:
    - Input for machine instructions and console input.
    - Output display for program results and feedback.
    - Buttons for loading, running, saving, and customizing the simulator.
    - Integration with a CPU and memory model for executing instructions.

    Attributes:
        instance_number (int): The identifier for this screen instance.
        memory (Memory): The memory object for storing instructions and data.
        input_handler (GUIInputHandler): Handles user input asynchronously.
        cpu (CPU): The CPU object for executing machine instructions.
        is_loaded (bool): Indicates if a program has been loaded.
        main_color (list): The primary theme color.
        off_color (list): The secondary (off) theme color.
    """

    def __init__(self, instance_number, **kwargs):
        """
        Initializes the UVSim screen with GUI elements and the simulator backend.

        Args:
            instance_number (int): The instance number of this screen.
            **kwargs: Additional arguments passed to the parent Screen initializer.
        """
        super().__init__(**kwargs)
        self.instance_number = instance_number

        # Initialize components
        self.memory = Memory(100)
        self.input_handler = GUIInputHandler(self)
        self.cpu = CPU(self.memory, self.input_handler)
        self.is_loaded = False

        # Theme colors
        self.main_color = theme[0]
        self.off_color = theme[1]

        # Main layout
        self.main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        # Left column
        left_column = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        with left_column.canvas.before:
            Color(*self.off_color)
            self.rect = Rectangle(size=left_column.size, pos=left_column.pos)
        left_column.bind(size=self._update_rect, pos=self._update_rect)

        # Machine Instructions Input
        self.machine_instructions_input = TextInput(
            hint_text='Machine Instructions',
            size_hint=(1, 0.3),
            multiline=True,
        )
        left_column.add_widget(self.machine_instructions_input)

        # Console Input
        self.console_input = TextInput(
            hint_text='Console Input',
            size_hint=(1, 0.1),
            multiline=False,
        )
        self.console_input.bind(on_text_validate=self.submit_console_input)
        self.console_input.disabled = True
        left_column.add_widget(self.console_input)

        # Output Display
        self.output_display = TextInput(
            hint_text='Output',
            size_hint=(1, 0.3),
            readonly=True,
            multiline=True,
        )
        left_column.add_widget(self.output_display)

        # Load Program Button
        self.load_button = Button(
            text='Load Program',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.load_button.bind(on_press=self.load_program)
        left_column.add_widget(self.load_button)

        # Run Button
        self.run_button = Button(
            text='Run Program',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.run_button.bind(on_press=self.run_program)
        left_column.add_widget(self.run_button)

        self.main_layout.add_widget(left_column)

        # Right column
        right_column = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        # Save File Button
        self.save_button = Button(
            text='Save File',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.save_button.bind(on_press=self.save_file)
        right_column.add_widget(self.save_button)

        # Pick File Button
        self.pick_file_button = Button(
            text='Pick File',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.pick_file_button.bind(on_press=self.pick_file)
        right_column.add_widget(self.pick_file_button)

        # Primary Color Input
        self.primary_color_input = TextInput(
            hint_text='Input primary color:',
            size_hint=(1, 0.1),
            multiline=False
        )
        right_column.add_widget(self.primary_color_input)

        # Off-Color Input
        self.off_color_input = TextInput(
            hint_text='Input off-color:',
            size_hint=(1, 0.1)
        )
        right_column.add_widget(self.off_color_input)

        # Submit Color Input Button
        self.submit_color_input_button = Button(
            text='Submit Custom Color Selection',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.submit_color_input_button.bind(on_press=self.pick_color)
        right_column.add_widget(self.submit_color_input_button)

        self.main_layout.add_widget(right_column)

        # Add the main_layout to the screen
        self.add_widget(self.main_layout)

        # Schedule asyncio event processing
        Clock.schedule_interval(self.process_asyncio_events, 0.1)

    def load_program(self, instance):
        """
        Loads machine instructions into memory from the GUI input.

        Args:
            instance: The Kivy Button instance that triggered this action.

        Displays:
            - Feedback in the output display on successful loading or errors.
        """
        machine_instructions = self.machine_instructions_input.text
        try:
            # Convert each line to an integer
            instructions = list(machine_instructions.strip().splitlines())

            # Load the program into memory
            self.cpu.memory.load_program(instructions)

            # Update the output display
            self.output_display.text += f"Program Loaded:\n{machine_instructions}\n"
        except Exception as e:
            self.output_display.text += f"Error: {e}.\n"
            return

        if not self.is_loaded:
            # First load: change button text to "Reload Program"
            self.load_button.text = "Reload Program"
            self.is_loaded = True
        else:
            # Reload: reinitialize CPU
            self.cpu = CPU(self.memory, self.input_handler)
            self.cpu.output_callback = self.output_callback
            self.output_display.text += "CPU Reinitialized.\n"

    def run_program(self, instance):
        """
        Starts the execution of the loaded program asynchronously.

        Args:
            instance: The Kivy Button instance that triggered this action.

        Displays:
            - Feedback in the output display during and after execution.
        """
        self.cpu.output_callback = self.output_callback
        self.output_display.text += "Running the program...\n"
        # Start the CPU execution asynchronously
        self.cpu.program_counter = 0
        asyncio.ensure_future(self.execute_cpu())

    async def execute_cpu(self):
        """
        Executes the CPU instructions until the program counter exceeds memory size.

        Handles:
            - Errors during execution and displays them in the output display.
        """
        try:
            while self.cpu.program_counter < self.memory.max_size:
                await self.cpu.execute_instruction()
        except Exception as e:
            self.output_display.text += f"Error: {e}\n"

    def save_file(self, instance):
        """
        Opens a file save dialog and saves the machine instructions to a file.

        Args:
            instance: The Kivy Button instance that triggered this action.
        """
        # Box layout for popup
        myBox = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Text input for file path
        self.file_path_input = TextInput(
            hint_text='Enter folder path to save the file',
            multiline=False
        )
        myBox.add_widget(self.file_path_input)

        # Save button to save the file
        save_button = Button(
            text='Save',
            size_hint_y=None,
            height=40
        )
        save_button.bind(on_press=self.confirm_save)
        myBox.add_widget(save_button)

        # Create the popup
        self.popup = Popup(title='Save File',
                           content=myBox,
                           size_hint=(0.9, 0.4))
        self.popup.open()

    def confirm_save(self, instance):
        """
        Confirms and saves the machine instructions to the specified file.

        Args:
            instance: The Kivy Button instance that triggered this action.

        Displays:
            - Feedback in the output display on success or error.
        """
        # Get file input from user
        folder_path = self.file_path_input.text.strip()
        file_name = "output.txt"  # Set your desired file name

        # Attempt to save the file in the specified folder
        try:
            full_path = os.path.join(folder_path, file_name)
            with open(full_path, 'w') as file:
                file.write(self.machine_instructions_input.text)  # Save the output to the file

            self.output_display.text += f"File saved successfully at {full_path}\n"
        except Exception as e:
            self.output_display.text += f"Error saving file: {e}\n"

        self.popup.dismiss()  # Close the popup after saving

    def pick_file(self, instance):
        """
        Opens a file chooser dialog for the user to load machine instructions.

        Args:
            instance: The Kivy Button instance that triggered this action.
        """
        # Opens a file chooser for the user to choose which file to load
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        filechooser = FileChooserListView()
        box.add_widget(filechooser)

        # Define a button to confirm the selection
        load_button = Button(text="Load", size_hint_y=None, height=40)
        box.add_widget(load_button)

        # Create the popup
        popup = Popup(title="Pick File", content=box, size_hint=(0.9, 0.9))
        popup.open()

        # Callback for when the user presses the Load button
        def on_load(button_instance):
            # Check if a file is selected
            if filechooser.selection:
                file_path = filechooser.selection[0]
                with open(file_path, 'r') as file:
                    self.machine_instructions_input.text = file.read()  # Load file contents
                self.output_display.text += f"File loaded from: {file_path}\n"
            popup.dismiss()  # Close popup after loading

        load_button.bind(on_press=on_load)  # Bind load button to function

    def pick_color(self, instance):
        """
        Updates the application's theme colors based on user input.

        Args:
            instance: The Kivy Button instance that triggered this action.
        """
        primary_color_input = ''
        off_color_input = ''
        if self.primary_color_input.text != "":
            primary_color_input = self.parse_color_input(self.primary_color_input.text)
            primary_color_input = primary_color_input if primary_color_input is not None else self.main_color
        if self.off_color_input.text != "":
            off_color_input = self.parse_color_input(self.off_color_input.text)
            off_color_input = off_color_input if off_color_input is not None else self.off_color

        try:
            theme[0] = primary_color_input
            theme[1] = off_color_input

            self.update_theme()
        except Exception as e:
            self.output_display.text += f"Error: {e}\n"

    def parse_color_input(self, color_input):
        """
        Parses and validates a color input in either hex (#RRGGBB) or rgba (r,g,b,a) format.

        Args:
            color_input (str): The color input string.

        Returns:
            list: A list representing the color as [r, g, b, a], or None if invalid.
        """
        # Check for hex format
        hex_match = re.match(r'^#([A-Fa-f0-9]{6})([A-Fa-f0-9]{2})?$', color_input.strip())
        if hex_match:
            hex_value = hex_match.group(1)
            if hex_match.group(2):  # If alpha channel is provided (8 characters total)
                alpha_value = hex_match.group(2)
            else:
                alpha_value = 'FF'  # Default to fully opaque if no alpha channel is provided

            # Convert hex values to rgba
            r = int(hex_value[0:2], 16) / 255
            g = int(hex_value[2:4], 16) / 255
            b = int(hex_value[4:6], 16) / 255
            a = int(alpha_value, 16) / 255
            return [r, g, b, a]

        # Check for r,g,b,a format
        try:
            rgba_values = list(map(float, color_input.strip().split(',')))
            if len(rgba_values) == 3:
                rgba_values.append(1.0)  # Add alpha = 1 (fully opaque) if not provided
            if len(rgba_values) == 4 and all(0 <= v <= 1 for v in rgba_values):
                return rgba_values
        except ValueError:
            pass

        # Invalid input if it doesn't match hex or rgba formats
        self.output_display.text += "Please input either hex values (with a # in front), or rgba values between 0 and 1.\n"
        return None

    def update_theme(self):
        """
        Updates the theme colors of all UI components based on the selected theme.
        """
        self.main_color = theme[0]
        self.off_color = theme[1]
        for button in [self.load_button, self.run_button, self.save_button, self.submit_color_input_button, self.pick_file_button]:
            button.background_color = self.main_color
        with self.main_layout.canvas.before:
            Color(*self.off_color)
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Updates the background rectangle's size and position when the layout changes.

        Args:
            instance: The instance triggering the change.
            value: The value to update the rect with
        """
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def submit_console_input(self, instance):
        """
        Handles console input submission and provides it to the input handler.

        Args:
            instance: The Kivy TextInput instance that triggered this action.
        """
        console_input_text = self.console_input.text
        self.output_display.text += f"Console Input: {console_input_text}\n"
        self.input_handler.provide_input(console_input_text)
        self.console_input.text = ''
        self.console_input.disabled = True  # Disable until next input is needed

    def enable_console_input(self):
        """
        Enables the console input field for user interaction, called by the input handler.
        """
        self.console_input.disabled = False
        self.console_input.focus = True

    def output_callback(self, message):
        """
        Handles CPU output by appending it to the output display.

        Args:
            message (str): The message to display.
        """
        self.output_display.text += f"{message}\n"

    def process_asyncio_events(self, dt):
        """
        Processes pending asyncio events for smooth integration with the Kivy event loop.

        Args:
            dt: The time interval since the last call.
        """
        try:
            # Process pending asyncio tasks
            self.input_handler.loop.call_soon_threadsafe(lambda: None)
            self.input_handler.loop.run_until_complete(asyncio.sleep(0))
        except Exception as e:
            self.output_display.text += f"Asyncio Error: {e}\n"

    def on_stop(self):
        """
        Cleans up resources and stops the asyncio event loop when the application exits.
        """
        # Clean up the asyncio loop on application exit
        self.input_handler.loop.stop()
