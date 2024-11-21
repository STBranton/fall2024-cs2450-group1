# main_layout.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView

from uv_sim_screen import UVSimScreen  # Import the UVSimScreen class


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Create a ScrollView for the tab bar (optional, for many tabs)
        scroll_view = ScrollView(size_hint_y=None, height=40)
        self.tab_bar = BoxLayout(orientation='horizontal', size_hint_x=None, height=40, padding=5, spacing=5)
        self.tab_bar.bind(minimum_width=self.tab_bar.setter('width'))
        scroll_view.add_widget(self.tab_bar)

        # Initialize ScreenManager
        self.screen_manager = ScreenManager()

        # Add tab_bar and screen_manager to the main layout
        self.add_widget(scroll_view)
        self.add_widget(self.screen_manager)

        # Initialize tab count
        self.instance_count = 0

        # Add "+" button first
        self.add_plus_button()

        # Add initial tab
        self.add_new_tab()

    def add_new_tab(self):
        self.instance_count += 1
        tab_name = f"Tab {self.instance_count}"
        screen_name = f"screen_{self.instance_count}"

        # Create tab button with a close button
        tab_button = BoxLayout(orientation='horizontal', size_hint=(None, 1), width=140)

        # Tab label
        label = Button(text=tab_name, size_hint=(None, 1), width=100, background_normal='', background_color=(0.1, 0.5, 0.8, 1))
        label.bind(on_release=lambda btn, name=screen_name: self.switch_tab(name))

        # Close button
        close_button = Button(text='x', size_hint=(None, 1), width=40, background_normal='', background_color=(1, 0, 0, 1))
        close_button.bind(on_release=lambda btn, tb=tab_button, sn=screen_name: self.close_tab(tb, sn))

        tab_button.add_widget(label)
        tab_button.add_widget(close_button)

        # Insert the new tab button before the "+" button
        self.tab_bar.remove_widget(self.plus_button)
        self.tab_bar.add_widget(tab_button)
        self.tab_bar.add_widget(self.plus_button)

        # Create new screen
        new_screen = UVSimScreen(instance_number=self.instance_count, name=screen_name)
        self.screen_manager.add_widget(new_screen)

        # Switch to the new tab
        self.switch_tab(screen_name)

    def add_plus_button(self):
        # Create "+" button
        self.plus_button = Button(text='+', size_hint=(None, 1), width=40, font_size='20sp', background_normal='', background_color=(0.2, 0.6, 1, 1))
        self.plus_button.bind(on_release=lambda x: self.add_new_tab())
        self.tab_bar.add_widget(self.plus_button)

    def switch_tab(self, screen_name):
        self.screen_manager.current = screen_name

    def close_tab(self, tab_button, screen_name):
        # Remove the screen from ScreenManager
        self.screen_manager.remove_widget(self.screen_manager.get_screen(screen_name))

        # Remove the tab button from the tab bar
        self.tab_bar.remove_widget(tab_button)

        # If the closed tab was active, switch to another tab
        if self.screen_manager.current == screen_name:
            if self.screen_manager.screen_names:
                # Switch to the last tab
                last_screen = self.screen_manager.screen_names[-1]
                self.switch_tab(last_screen)
            else:
                self.instance_count = 0  # Reset count if no tabs left
