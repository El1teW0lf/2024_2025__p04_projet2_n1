from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenText
from panda3d.core import TextNode


class PauseMenu:
    def __init__(self, base):
        self.base = base

        self.menu_frame = DirectFrame(
            frameColor=(0, 0, 0, 0.7),  
            frameSize=(-0.5, 0.5, -0.5, 0.5),  
            pos=(0, 0, 0) ,
            sortOrder=1
        )

<<<<<<< HEAD
        self.background_frame = DirectFrame(
            parent=self.menu_frame,
            frameSize=(-0.5, 0.5, -0.5, 0.5),  # Match the menu frame size
            frameTexture="assets/pause_menu_bg.png",  # Replace with your image path
            frameColor=(1, 1, 1, 1),  # Ensure the texture color shows up correctly
            pos=(0, 0, 0)
        )

        self.base.base.ui["pause_menu"] = self.menu_frame
=======
        self.base.main.ui["pause_menu"] = self.menu_frame
>>>>>>> fc849d67fafc59c9be6791a6277b5fca79566694

        self.title = OnscreenText(
            text="Main Menu",
            parent=self.menu_frame,
            scale=0.1,
            pos=(0, 0.35),
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )

        self.resume_button = DirectButton(
            text="Resume",
            scale=0.07,
            command=self.base.toggle_pause_menu,
            parent=self.menu_frame,
            pos=(0, 0, 0.1),
        )

        self.quit_button = DirectButton(
            text="Quit",
            scale=0.07,
            command=self.exit_game,
            parent=self.menu_frame,
            pos=(0, 0, -0.1),
        )

        self.menu_frame.hide()

    def show(self):
        """Show the menu."""
        self.menu_frame.show()

    def hide(self):
        """Hide the menu."""
        self.menu_frame.hide()

    def exit_game(self):
        """Exit the game."""
        print("Exiting the game...")
        self.base.userExit()
