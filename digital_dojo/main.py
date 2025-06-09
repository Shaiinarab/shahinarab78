from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button
from textual.containers import Container
from textual.screen import Screen

# Assuming views.py is in digital_dojo.ui
from digital_dojo.ui.views import HabitsScreen, JournalScreen, UrgeLogScreen

class MainMenuScreen(Screen):
    """The main menu screen for the Digital Dojo app."""

    TITLE = "The Digital Dojo - Main Menu"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Button("View Habits", id="view_habits", variant="primary"),
            Button("Open Journal", id="open_journal", variant="primary"),
            Button("Log Urge", id="log_urge", variant="primary"),
            Button("Exit App", id="exit_app", variant="error")
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "view_habits":
            self.app.push_screen(HabitsScreen())
        elif event.button.id == "open_journal":
            self.app.push_screen(JournalScreen())
        elif event.button.id == "log_urge":
            self.app.push_screen(UrgeLogScreen())
        elif event.button.id == "exit_app":
            self.app.exit()


class DigitalDojoApp(App):
    """The main application class for The Digital Dojo."""

    TITLE = "The Digital Dojo"
    CSS_PATH = "main.tcss" # Relative to the App class / main.py

    # SCREENS dictionary can be used to manage screens if preferred,
    # but push_screen by name/instance also works well.
    # SCREENS = {
    #     "main_menu": MainMenuScreen(),
    #     "habits": HabitsScreen(),
    #     "journal": JournalScreen(),
    #     "urge_log": UrgeLogScreen(),
    # }

    def on_mount(self) -> None:
        """Called when app starts."""
        # Start with the main menu
        self.push_screen(MainMenuScreen())


if __name__ == "__main__":
    app = DigitalDojoApp()
    app.run()
