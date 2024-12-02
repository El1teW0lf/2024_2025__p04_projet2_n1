from direct.gui.DirectGui import DirectButton, DirectLabel,DirectFrame, DGG
from panda3d.core import TextNode


class MainMenu():
    def __init__(self,base,launch_function):
        self.on_launch = launch_function
        self.base = base
        self.setup_main_menu()

    def setup_main_menu(self):


        self.aspect_ratio = self.base.getAspectRatio()
        self.font = self.base.loader.loadFont("ui/Jellies.ttf")

        self.base.ui["start_menu"] = []

 
        self.frame = DirectFrame(
            frameSize=(-self.aspect_ratio, self.aspect_ratio, -1, 1),  
            pos=(0, 0, 0) ,
            sortOrder=1,
            frameTexture = "ui/bg_green.png"
        )

        self.title = DirectLabel(
            text="Main Menu",
            scale=0.1,
            pos=(0, 0, 0.7),
            text_fg=(1, 1, 1, 1),
            text_align=TextNode.ACenter,
            parent=self.frame,
            text_font = self.font
        )


        self.start_button = DirectButton(
            scale=1, 
           
            relief=DGG.FLAT,
            frameSize=(-1, 1, -0.1, 0.1),
            pos=(0, 0, 0.2),
            command=self.start_game,
            parent=self.frame,
            frameTexture = self.base.loader.loadTexture("ui/play_icon_text.png"),
        )
        self.settings_button = DirectButton(
            text="Settings",
            scale=0.08,
            pos=(0, 0, 0),
            command=self.show_settings,
             parent=self.frame,
            text_font = self.font
        )
        self.quit_button = DirectButton(
            text="Quit",
            scale=0.08,
            pos=(0, 0, -0.2),
            command=self.quit_game,
            parent=self.frame,
            text_font = self.font
        )

        self.base.ui["start_menu"].append(self.frame)

    def start_game(self):
        print("Start Game clicked!")
        self.on_launch()


    def show_settings(self):
        print("Settings clicked!")

    def quit_game(self):
        print("Quit clicked!")
        self.base.userExit()

