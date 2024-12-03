from direct.gui.DirectGui import DirectFrame, DirectButton, OnscreenText
from panda3d.core import TextNode, TransparencyAttrib


class PauseMenu:
    def __init__(self, base):
        self.base = base

        # Get the aspect ratio to calculate fullscreen coordinates
        aspect_ratio = base.main.getAspectRatio()

        # Fullscreen background frame (hidden initially)
        self.background_frame = DirectFrame(
            frameSize=(-aspect_ratio, aspect_ratio, -1, 1),  # Fullscreen coordinates
            frameTexture="menus/assets/Background_Green.png",  # Replace with your image path
            frameColor=(1, 1, 1, 1),  # Fully transparent frame, texture still visible
            parent=base.main.aspect2d,  # Parent it to aspect2d for proper scaling
            sortOrder=0  # Ensure it is drawn behind the menu
        )
        self.background_frame.hide()  # Initially hidden

        # Main menu frame (overlay, hidden initially)
        self.menu_frame = DirectFrame(
            frameColor=(1, 1, 1, 0),  
            frameSize=(-aspect_ratio, aspect_ratio, -1, 1),  
            pos=(0, 0, 0),  
            parent=base.main.aspect2d,  # Parent it to aspect2d for proper scaling
            sortOrder=1  # Ensure it is drawn above the background
        )
        self.menu_frame.hide()  # Initially hidden

        # Add the menu to the UI dictionary for potential external control
        self.base.main.ui["pause_menu"] = self.menu_frame

        # Title text
        self.title = OnscreenText(
            text="Pause Menu",
            parent=self.menu_frame,
            scale=0.1,
            pos=(0, 0.35),
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter
        )

        # Resume button
        self.resume_button = DirectButton(
            image = "menus/assets/resume_button.png",
            text="",
            scale= (0.5, 1.2, 0.15),
            command=self.base.toggle_pause_menu,  # Toggles the menu visibility
            parent=self.menu_frame,
            pos=(0, 0, 0.1),
            
        )

        # Quit button
        self.quit_button = DirectButton(
            text="Quit",
            scale=0.07,
            command=self.exit_game,  # Exits the game
            parent=self.menu_frame,
            pos=(0, 0, -0.1),
        )

    def show(self):
        """Show the pause menu and background."""
        self.background_frame.show()
        self.menu_frame.show()
        self.resume_button.setColor(1, 1, 1, 0)
        self.resume_button.setTransparency(TransparencyAttrib.MAlpha)

    def hide(self):
        """Hide the pause menu and background."""
        self.background_frame.hide()
        self.menu_frame.hide()

    def exit_game(self):
        """Exit the game."""
        print("Exiting the game...")
        self.base.userExit()
