"""
Main GUI File, run this file to start the GUI
"""
from kivy.app import App

from main_layout import MainLayout


class UVSimApp(App):
    """
    A Kivy-based application for running the UVSim simulator.

    This application uses a custom main layout (`MainLayout`) and manages the
    lifecycle of all screens, ensuring proper cleanup when the app stops.
    """

    def build(self):
        """
        Builds and returns the root widget for the application.

        Returns:
            MainLayout: The main layout of the application.
        """
        return MainLayout()

    def on_stop(self):
        """
        Called when the application is stopping.

        Ensures that all screens in the `screen_manager` stop any ongoing processes
        or loops properly to avoid issues with resource management or hanging threads.
        """
        for screen in self.root.screen_manager.screens:
            screen.on_stop()


if __name__ == '__main__':
    UVSimApp().run()
