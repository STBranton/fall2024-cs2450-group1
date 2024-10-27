import asyncio
import re
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

from cpu import CPU
from input_handler import GUIInputHandler
from memory import Memory

theme = [
        [76/255, 114/255, 29/255, 1], #dark green
        [255, 255, 255, 1], #white
]


class UVSimApp(App):
    def build(self):

        self.memory = Memory(100)
        self.input_handler = GUIInputHandler(self)
        # Initialize CPU without an output callback initially
        self.is_loaded = False
        self.cpu = CPU(self.memory, self.input_handler)

        #self.current_theme = "primary"
        self.main_color = theme[0]
        self.off_color = theme[1]

        
        self.main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        left_column = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        with self.main_layout.canvas.before:
            Color(*self.off_color)
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self._update_rect, pos=self._update_rect)

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
        right_column = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        # save_file button
        self.save_button = Button(
            text='Save File',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.save_button.bind(on_press=self.save_file)
        right_column.add_widget(self.save_button)

        # pick_file button
        self.pick_file_button = Button(
            text='Pick File',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.pick_file_button.bind(on_press=self.pick_file)
        right_column.add_widget(self.pick_file_button)

        # Create a horizontal layout for the new buttons
        #button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        # Primary Color Input
        self.primary_color_input = TextInput(
            hint_text='Input primary color:',
            size_hint=(1, 0.1),
            multiline=False
        )
        right_column.add_widget(self.primary_color_input)

        # Off-Color input
        self.off_color_input = TextInput(
            hint_text='Input off-color:',
            size_hint=(1, 0.1)
        )
        right_column.add_widget(self.off_color_input)

        # submit colour input button
        self.submit_color_input_button = Button(
            text='Submit custom color selection',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        self.submit_color_input_button.bind(on_press=self.pick_color)
        right_column.add_widget(self.submit_color_input_button)


        self.main_layout.add_widget(right_column)

        return self.main_layout


    def load_program(self, instance):
        machine_instructions = self.machine_instructions_input.text
        try:
            # Convert each line to an integer
            instructions = list(map(int, machine_instructions.strip().splitlines()))

            # Load the program into memory
            self.cpu.memory.load_program(instructions)

            # Update the output display
            self.output_display.text += f"Program Loaded:\n{machine_instructions}\n"
        except ValueError:
            self.output_display.text += "Error: Invalid instructions. Please ensure all lines contain integers.\n"
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
        self.cpu.output_callback = self.output_callback
        self.output_display.text += "Running the program...\n"
        # Start the CPU execution asynchronously
        self.cpu.program_counter = 0
        asyncio.ensure_future(self.execute_cpu())

    async def execute_cpu(self):
        try:
            while self.cpu.program_counter < self.memory.max_size:
                await self.cpu.execute_instruction()
        except Exception as e:
            self.output_display.text += f"Error: {e}\n"

    def save_file(self, instance):
        #box layout for popup
        myBox = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        #text input for file path
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

        # make the pop up
        self.popup = Popup(title='Save File',
                        content=myBox,
                        size_hint=(0.9, 0.4))
        self.popup.open()

    def confirm_save(self, instance):
        #get file input from user
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
        #Opens a file chooser for the user to choose which file to load
        myBox = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        myBox.add_widget(filechooser)

        # Define a button to confirm the selection
        load_button = Button(text="Load")
        myBox.add_widget(load_button)

        # Popup to hold the file chooser
        popup = Popup(title="Pick File", content=myBox, size_hint=(0.9, 0.9))
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
        Parse and validate a color input in either hex format (#RRGGBB, #RRGGBBAA)
        or r,g,b,a format. Returns a list of [r, g, b, a] with values in range 0 to 1.
        Returns None if the input is invalid.
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
            self.main_color = theme[0]
            self.off_color = theme[1]
            for button in [self.load_button, self.run_button, self.save_button, self.submit_color_input_button, self.pick_file_button]:
                button.background_color = self.main_color
            with self.main_layout.canvas.before:
                Color(*self.off_color)
                self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
            self.main_layout.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


    def submit_console_input(self, instance):
        console_input_text = self.console_input.text
        self.output_display.text += f"Console Input: {console_input_text}\n"
        self.input_handler.provide_input(console_input_text)
        self.console_input.text = ''
        self.console_input.disabled = True  # Disable until next input is needed

    def enable_console_input(self):
        """
        Called by GUIInputHandler to enable the console input field.
        """
        self.console_input.disabled = False
        self.console_input.focus = True

    def output_callback(self, message):
        """
        Receives output from the CPU and displays it in the GUI.
        """
        self.output_display.text += f"{message}\n"

    def on_start(self):
        # Integrate asyncio event loop with Kivy
        Clock.schedule_interval(self.process_asyncio_events, 0.1)

    def process_asyncio_events(self, dt):
        try:
            # Process pending asyncio tasks
            self.input_handler.loop.call_soon_threadsafe(lambda: None)
            self.input_handler.loop.run_until_complete(asyncio.sleep(0))
        except Exception as e:
            self.output_display.text += f"Asyncio Error: {e}\n"

    def on_stop(self):
        # Clean up the asyncio loop on application exit
        self.input_handler.loop.stop()

if __name__ == '__main__':
    UVSimApp().run()
