from direct.showbase.ShowBase import ShowBase
from panda3d.core import *  
from direct.gui.DirectGui import *
from direct.task import Task
from modules import parse_json
import os

class Test_World(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.disableMouse()  # Disable default mouse-driven camera control
        
        self.setBackgroundColor(0, 0, 0)

        # Set initial camera position
        self.camera.setPos(0, 0, 45)
        self.camera.setHpr(0, -90, 0)

        # Movement variables
        self.speed = 100  # Movement speed
        self.key_map = {
            "z": False,  # Move forward
            "s": False,  # Move backward
            "q": False,  # Move left
            "d": False,   # Move right
            "control": False, #Down
            "space": False, #UP
        }

        # Mouse sensitivity
        self.mouse_sensitivity = 10

        # Lock mouse to center
        self.lock_mouse()

        # Create OnscreenText for displaying position and direction
        self.info_text = OnscreenText(
            text="", pos=(-1.3, 0.9), scale=0.05, align=TextNode.ALeft, 
            fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5), parent=self.aspect2d
        )

        # Accept key inputs
        self.accept("z", self.update_key_map, ["z", True])
        self.accept("z-up", self.update_key_map, ["z", False])
        self.accept("s", self.update_key_map, ["s", True])
        self.accept("s-up", self.update_key_map, ["s", False])
        self.accept("q", self.update_key_map, ["q", True])
        self.accept("q-up", self.update_key_map, ["q", False])
        self.accept("d", self.update_key_map, ["d", True])
        self.accept("d-up", self.update_key_map, ["d", False])
        self.accept("control", self.update_key_map, ["control", True])
        self.accept("control-up", self.update_key_map, ["control", False])
        self.accept("space", self.update_key_map, ["space", True])
        self.accept("space-up", self.update_key_map, ["space", False])

        # Tasks to update camera position, direction, and text
        self.taskMgr.add(self.update_camera, "UpdateCamera")
        self.taskMgr.add(self.update_camera_direction, "UpdateCameraDirection")
        self.taskMgr.add(self.update_info_text, "UpdateInfoText")

        script_directory = os.path.dirname(os.path.realpath(__file__))
        folder_path = os.path.join(script_directory, "test_scene")

        parse_json(folder_path,self.render,self.loader,"scenes/test_scene")
        
    def lock_mouse(self):
        """Locks the mouse to the center of the window."""
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_absolute)
        self.win.requestProperties(props)
        self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)

    def update_key_map(self, key, state):
        """Updates the state of key_map when a key is pressed/released."""
        self.key_map[key] = state

    def update_camera(self, task):
        """Moves the camera based on WASD keys."""
        dt = globalClock.getDt()  # Get the time since the last frame

        # Get the camera's current position
        pos = self.camera.getPos()
        hpr = self.camera.getHpr()

        # Movement directions
        forward = self.camera.getQuat().getForward() * self.speed * dt
        right = self.camera.getQuat().getRight() * self.speed * dt
        up = self.camera.getQuat().getUp() * self.speed * dt

        # Apply movement
        if self.key_map["z"]:
            self.camera.setPos(pos + forward)
        if self.key_map["s"]:
            self.camera.setPos(pos - forward)
        if self.key_map["q"]:
            self.camera.setPos(pos - right)
        if self.key_map["d"]:
            self.camera.setPos(pos + right)
        if self.key_map["control"]:
            self.camera.setPos(pos - up)
        if self.key_map["space"]:
            self.camera.setPos(pos + up)

        return Task.cont  # Continue the task
    
    def update_camera_direction(self, task):
        """Adjusts the camera direction based on mouse movement."""
        # Get the current mouse position
        if self.mouseWatcherNode.hasMouse():
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()

            # Rotate the camera based on mouse movement
            h = self.camera.getH() - x * self.mouse_sensitivity   # Add 90 degrees to initial heading
            p = self.camera.getP() + y * self.mouse_sensitivity
            self.camera.setHpr(h, p, 0)

            # Reset the mouse to the center
            self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)

        return Task.cont

    def update_info_text(self, task):
        """Updates the onscreen text with the camera's position and direction."""
        pos = self.camera.getPos()
        hpr = self.camera.getHpr()
        self.info_text.setText(
            f"Position: x={pos.x:.2f}, y={pos.y:.2f}, z={pos.z:.2f}\n"
            f"Direction: h={hpr.x:.2f}, p={hpr.y:.2f}, r={hpr.z:.2f}"
        )
        return Task.cont
    
    def load_sub(self):
        self.sub = loader.loadModel("models/submarine/psx_sub_free.fbx")
        self.sub.reparentTo(render)
        self.sub_tex = loader.loadTexture("models/submarine/Glass.jpg")
        self.sub.setTexture(self.sub_tex, 1)

        print(self.sub.getPos())