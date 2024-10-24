import asyncio

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from cpu import CPU
from input_handler import GUIInputHandler
from memory import Memory


theme = {
    "default": [
        [76/255, 114/255, 29/255, 1], #dark green
        [255, 255, 255, 1], #white
        [0.9/255, 0.9/255, 0.9/255, 1] #light gray
    ],

    "primary": [
        [0, 0, 1, 1], #true blue
        [0.68, 0.85, 0.9, 1], #light blue
        [128/255, 128/255, 128/255, 1] #medium gray
    ],
}


class UVSimApp(App):
    def build(self):

        self.memory = Memory(100)
        self.input_handler = GUIInputHandler(self)
        # Initialize CPU without an output callback initially
        self.is_loaded = False
        self.cpu = CPU(self.memory, self.input_handler)

        self.current_theme = "default"
        #self.current_theme = "primary"
        self.main_color = theme[self.current_theme][0]
        self.off_color = theme[self.current_theme][1]
        self.secondary_color = theme[self.current_theme][2]

        
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        left_column = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        # Machine Instructions Input
        self.machine_instructions_input = TextInput(
            hint_text='Machine Instructions',
            size_hint=(1, 0.3),
            multiline=True,
            background_color=self.off_color
        )
        left_column.add_widget(self.machine_instructions_input)

        # Console Input
        self.console_input = TextInput(
            hint_text='Console Input',
            size_hint=(1, 0.1),
            multiline=False,
            background_color=self.off_color
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
            background_color=self.off_color
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
        run_button = Button(
            text='Run Program',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        run_button.bind(on_press=self.run_program)
        left_column.add_widget(run_button)

        main_layout.add_widget(left_column)
        right_column = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        # save_file button
        save_button = Button(
            text='Save File',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        save_button.bind(on_press=self.save_file)
        right_column.add_widget(save_button)

        # pick_file button
        pick_file_button = Button(
            text='Pick File',
            size_hint=(1, 0.1),
            background_color=self.main_color
        )
        pick_file_button.bind(on_press=self.pick_file)
        right_column.add_widget(pick_file_button)

        # Create a horizontal layout for the new buttons
        #button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        # Primary Color Input
        self.primary_input = TextInput(
            hint_text='Input primary color:',
            size_hint=(1, 0.1),
            multiline=False
        )
        right_column.add_widget(self.primary_input)

        # Off-Color input
        self.off_color_input = TextInput(
            hint_text='Input off-color:',
            size_hint=(1, 0.1)
        )
        right_column.add_widget(self.off_color_input)

        # pick_color button
        pick_color_button = Button(
            text='Submit custom color selection',
            size_hint=(1, 0.1),
            #background_color=self.main_color
        )
        pick_color_button.bind(on_press=self.pick_color)
        right_column.add_widget(pick_color_button)


        main_layout.add_widget(right_column)
        return main_layout

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
        asyncio.ensure_future(self.execute_cpu())

    async def execute_cpu(self):
        try:
            while self.cpu.program_counter < self.memory.max_size:
                await self.cpu.execute_instruction()
        except Exception as e:
            self.output_display.text += f"Error: {e}\n"

    def save_file(self, instance):
        pass

    def pick_file(self, instance):
        pass

    def pick_color(self, instance):
        pass

    def change_primary_color(self, instance):
        # Logic to change the primary color
        self.primary_color = [1, 0, 0, 1]  # Example: Change to red
        self.update_colors()

    def change_off_color(self, instance):
        # Logic to change the off color
        self.off_color = [0, 0, 1, 1]  # Example: Change to blue
        self.update_colors()

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
