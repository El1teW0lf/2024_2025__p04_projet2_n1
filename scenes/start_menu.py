from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectLabel
from panda3d.core import TextNode


class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_main_menu()

    def setup_main_menu(self):

        # Title
        self.title = DirectLabel(
            text="Main Menu",
            scale=0.1,
            pos=(0, 0, 0.7),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text_align=TextNode.ACenter
        )

        # Buttons
        self.start_button = DirectButton(
            text="Start Game",
            scale=0.08,
            pos=(0, 0, 0.2),
            command=self.start_game
        )
        self.settings_button = DirectButton(
            text="Settings",
            scale=0.08,
            pos=(0, 0, 0),
            command=self.show_settings
        )
        self.quit_button = DirectButton(
            text="Quit",
            scale=0.08,
            pos=(0, 0, -0.2),
            command=self.quit_game
        )

    def start_game(self):
        print("Start Game clicked!")
        # Transition to the game scene or logic here

    def show_settings(self):
        print("Settings clicked!")
        # Add logic to show a settings menu

    def quit_game(self):
        print("Quit clicked!")
        self.userExit()


if __name__ == "__main__":
    app = MainMenu()
    app.run()
