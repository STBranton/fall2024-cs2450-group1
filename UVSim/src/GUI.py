from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class UVSimApp(App):
    def build(self):
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
        self.console_input.bind(on_text_validate=self.submit_console_input)  # Bind Enter key event
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
        load_button = Button(
            text='Load Program',
            size_hint=(1, 0.1)
        )
        load_button.bind(on_press=self.load_program)
        layout.add_widget(load_button)

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
        self.output_display.text += f"Program Loaded:\n{machine_instructions}\n"

    def run_program(self, instance):
        self.output_display.text += "Running the program...\n"

    def submit_console_input(self, instance):
        # Get the text from console input and print it
        console_input_text = self.console_input.text
        #self.output_display.text += f"Console Input: {console_input_text}\n"  # Display in output area
        print(console_input_text)  # Print to terminal
        self.console_input.text = ''  # Clear the input field after submission

if __name__ == '__main__':
    UVSimApp().run()


'''
variable: machine_instructions: holds multiline machine instructions
variable: console_input_text: hold the single inputs

'''