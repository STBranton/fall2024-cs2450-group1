import asyncio

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from cpu import CPU
from input_handler import GUIInputHandler
from memory import Memory


class UVSimApp(App):
    def build(self):
        # Initialize memory
        self.memory = Memory(100)
        self.input_handler = GUIInputHandler(self)
        # Initialize CPU without an output callback initially
        self.is_loaded = False
        self.cpu = CPU(self.memory, self.input_handler)

        # Layout setup
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Machine Instructions Input
        self.machine_instructions_input = TextInput(
            hint_text='Machine Instructions',
            size_hint=(1, 0.3),
            multiline=True
        )
        layout.add_widget(self.machine_instructions_input)

        # Console Input
        self.console_input = TextInput(
            hint_text='Console Input',
            size_hint=(1, 0.1),
            multiline=False  # This makes it a single line
        )
        self.console_input.bind(on_text_validate=self.submit_console_input)
        self.console_input.disabled = True  # Initially disabled
        layout.add_widget(self.console_input)

        # Output Display
        self.output_display = TextInput(
            hint_text='Output',
            size_hint=(1, 0.3),
            readonly=True,
            multiline=True
        )
        layout.add_widget(self.output_display)

        # Load Program Button
        self.load_button = Button(
            text='Load Program',
            size_hint=(1, 0.1)
        )
        self.load_button.bind(on_press=self.load_program)
        layout.add_widget(self.load_button)

        # Run Button
        run_button = Button(
            text='Run Program',
            size_hint=(1, 0.1)
        )
        run_button.bind(on_press=self.run_program)
        layout.add_widget(run_button)

        return layout

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
