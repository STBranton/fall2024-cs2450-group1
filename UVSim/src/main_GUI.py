from kivy.app import App

from main_layout import MainLayout


class UVSimApp(App):
    def build(self):
        return MainLayout()

    def on_stop(self):
        # Ensure all asyncio loops are stopped properly
        for screen in self.root.screen_manager.screens:
            screen.on_stop()

if __name__ == '__main__':
    UVSimApp().run()
