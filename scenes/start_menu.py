from direct.gui.DirectGui import DirectButton, DirectLabel
from panda3d.core import TextNode


class MainMenu():
    def __init__(self,base,launch_function):
        self.on_launch = launch_function
        self.base = base
        self.setup_main_menu()

    def setup_main_menu(self):

        self.base.ui["start_menu"] = []

        self.title = DirectLabel(
            text="Main Menu",
            scale=0.1,
            pos=(0, 0, 0.7),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text_align=TextNode.ACenter
        )


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

        self.base.ui["start_menu"].append(self.title)
        self.base.ui["start_menu"].append(self.start_button)
        self.base.ui["start_menu"].append(self.settings_button)
        self.base.ui["start_menu"].append(self.quit_button)

    def start_game(self):
        print("Start Game clicked!")
        self.on_launch()


    def show_settings(self):
        print("Settings clicked!")

    def quit_game(self):
        print("Quit clicked!")
        self.base.userExit()

