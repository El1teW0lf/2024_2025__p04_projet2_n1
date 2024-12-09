from direct.gui.DirectGui import DirectFrame, DirectButton
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import DirectButton, DirectLabel, DirectFrame, DGG
from panda3d.core import TextNode, NodePath, GeomNode, Plane, CardMaker
from panda3d.core import Texture, Vec3
from panda3d.core import Shader
from panda3d.core import TransparencyAttrib
from panda3d.core import CollisionRay, CollisionNode, CollisionTraverser, CollisionHandlerQueue, GeomNode
from panda3d.bullet import BulletTriangleMesh, BulletRigidBodyNode, BulletTriangleMeshShape, BulletBoxShape
from panda3d.bullet import BulletDebugNode
from panda3d.core import CollisionNode, CollisionBox, CollisionHandlerQueue, CollisionTraverser
from panda3d.core import TransparencyAttrib, CardMaker

class PauseMenu():
    def __init__(self, base, launch_function):
        super().__init__()
        self.on_launch = launch_function
        self.main = base
        self.main.reset()
        self.main.disableMouse()
        self.size_factor = 256 * 1.2

        self.width = self.main.win.getXsize()
        self.height = self.main.win.getYsize()
        self.bullet_world = self.main.bullet_world

        self.show_debug_collision = True

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(self.show_debug_collision)
        debugNode.showConstraints(self.show_debug_collision)
        debugNode.showBoundingBoxes(self.show_debug_collision)
        debugNode.showNormals(self.show_debug_collision)
        debugNP = self.main.render.attachNewNode(debugNode)
        debugNP.show()

        # Get the aspect ratio to calculate fullscreen coordinates
        aspect_ratio = base.main.getAspectRatio()

        self.bullet_world.setDebugNode(debugNP.node())

        self.picker_ray = CollisionRay()
        self.picker_node = CollisionNode("mouseRay")
        self.picker_node.addSolid(self.picker_ray)
        self.picker_node.setFromCollideMask(GeomNode.getDefaultCollideMask())  # Detect all geometry
        self.picker_np = self.main.camera.attachNewNode(self.picker_node)

        # Collision traverser and handler
        self.collision_traverser = CollisionTraverser()
        self.collision_handler = CollisionHandlerQueue()
        self.collision_traverser.addCollider(self.picker_np, self.collision_handler)

        # Mouse click detection
        self.main.accept("mouse1", self.on_click)

        self.create_bg()
        self.start_play_button = self.create_button("start_play_button", -1.45, 6.75, 0.05, 280 / self.size_factor, 90 / self.size_factor)
        self.start_settings_button = self.create_button("start_settings_button", -1.2, 6.75, -0.4, 450 / self.size_factor, 90 / self.size_factor)
        self.start_quit_button = self.create_button("start_quit_button", -1.45, 6.75, -0.85, 280 / self.size_factor, 90 / self.size_factor)
        self.start_logo = self.create_button("start_logo", -1.0, 6.75, 1, 810 / self.size_factor, 340 / self.size_factor)
        texture = self.main.loader.loadTexture("ui/nice_logo.png")
        texture.setMinfilter(Texture.FTLinear) 
        texture.setMagfilter(Texture.FTLinear)
        self.start_logo.setTexture(texture)
        self.start_logo.setColor(1, 1, 1, 1)  

        # Fullscreen background frame (hidden initially)
        self.background_frame = DirectFrame(
            frameSize=(-aspect_ratio, aspect_ratio, -1, 1),  # Fullscreen coordinates
            frameTexture="menus/assets/pause_menu/Background_Green.png",  # Replace with your image path
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
            image="menus/assets/pause_menu/paused_text.png",  # Path to your title image
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
            image="menus/assets/pause_menu/resume_button.png",
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
            image="menus/assets/pause_menu/settings_button.png",
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
            image="menus/assets/pause_menu/save_button.png",
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
            image="menus/assets/pause_menu/quit_button.png",
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
