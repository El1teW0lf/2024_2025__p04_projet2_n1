from direct.gui.DirectGui import DirectFrame, DirectButton
from panda3d.core import TransparencyAttrib


class PauseMenu:
    def __init__(self, base):
        self.base = base

        # Get the aspect ratio to calculate fullscreen coordinates
        aspect_ratio = base.main.getAspectRatio()

        # Fullscreen background frame (hidden initially)
        self.background_frame = DirectFrame(
            frameSize=(-aspect_ratio, aspect_ratio, -1, 1),  # Fullscreen coordinates
            frameTexture="menus/assets/Background_Green.png",  # Replace with your image path
            frameColor=(1, 1, 1, 1),  # Fully visible frame, texture still visible
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

        # Title image
        self.title_image = DirectFrame(
            image="menus/assets/paused_text.png",  # Path to your title image
            parent=self.menu_frame,
            frameColor=(1, 1, 1, 0),
            scale=(0.5, 1.2, 0.15),  # Adjust the scale to fit your menu
            pos=(0, -0.2, 0.8),  # Position the image appropriately
        )
        self.title_image.setTransparency(TransparencyAttrib.MAlpha)  # Enable transparency

        # Common vertical spacing between buttons
        spacing = 0.35
        starting_y = 0.3  # Y-coordinate of the first button
        x_position = 0  # Horizontal alignment for all buttons

        # Resume button
        self.resume_button = DirectButton(
            image="menus/assets/resume_button.png",
            text="",
            frameColor=(1, 1, 1, 0),
            scale=(0.6, 1.2, 0.15),
            command=self.base.toggle_pause_menu,  # Toggles the menu visibility
            parent=self.menu_frame,
            pos=(x_position, 0, starting_y),
        )
        self.resume_button.setTransparency(TransparencyAttrib.MAlpha)

        # Settings button
        self.settings_button = DirectButton(
            image="menus/assets/settings_button.png",
            text="",
            frameColor=(1, 1, 1, 0),
            scale=(0.7, 1.2, 0.15),
            command=self.open_settings,  # Opens settings menu
            parent=self.menu_frame,
            pos=(x_position + 0.1, 0, starting_y - spacing),
        )
        self.settings_button.setTransparency(TransparencyAttrib.MAlpha)

        # Save button
        self.save_button = DirectButton(
            image="menus/assets/save_button.png",
            text="",
            frameColor=(1, 1, 1, 0),
            scale=(0.6, 1.2, 0.15),
            command=self.save_game,  # Saves the game
            parent=self.menu_frame,
            pos=(x_position, 0, starting_y - 2 * spacing),
        )
        self.save_button.setTransparency(TransparencyAttrib.MAlpha)

        # Quit button
        self.quit_button = DirectButton(
            image="menus/assets/quit_button.png",
            text="",
            frameColor=(1, 1, 1, 0),
            scale=(0.5, 1.2, 0.15),
            command=self.exit_game,  # Exits the game
            parent=self.menu_frame,
            pos=(x_position - 0.1, 0, starting_y - 3 * spacing),
        )
        self.quit_button.setTransparency(TransparencyAttrib.MAlpha)

    def show(self):
        """Show the pause menu and background."""
        self.background_frame.show()
        self.menu_frame.show()

    def hide(self):
        """Hide the pause menu and background."""
        self.background_frame.hide()
        self.menu_frame.hide()

    def open_settings(self):
        """Open the settings menu."""
        print("Opening the settings")

    def save_game(self):
        """Save the game."""
        print("Saving the game...")

    def exit_game(self):
        """Exit the game."""
        print("Exiting the game...")
        self.base.userExit()
