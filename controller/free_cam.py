from panda3d.core import (
    BitMask32, WindowProperties, TextNode
)
from panda3d.bullet import (
    BulletWorld, BulletRigidBodyNode, BulletSphereShape, BulletCharacterControllerNode,
    BulletCapsuleShape,BulletSphereShape
)
from panda3d.core import NodePath, Point3, Vec3, Quat
from direct.gui.DirectGui import OnscreenText
from direct.task import Task
from direct.showbase.ShowBaseGlobal import globalClock


class FreeCameraController:
    def __init__(self, base):
        self.base = base
        self.speed = 1000
        self.paused = False
        self.mouse_free = False
        self.h = 0
        self.p = 0
        self.key_map = {
            "z": False, 
            "s": False,  
            "q": False,  
            "d": False,  
            "control": False, 
            "space": False,  
        }
        self.mouse_sensitivity = 10

        self.lock_mouse()

        self.info_text = OnscreenText(
            text="", pos=(-1.3, 0.9), scale=0.05, align=TextNode.ALeft, 
            fg=(1, 1, 1, 1), shadow=(0, 0, 0, 0.5), parent=self.base.aspect2d
        )

        self.accept_inputs()

        # Initialize Bullet physics system
        self.init_bullet()

        self.base.taskMgr.add(self.update_camera, "UpdateCamera")
        self.base.taskMgr.add(self.update_camera_direction, "UpdateCameraDirection")
        self.base.taskMgr.add(self.update_info_text, "UpdateInfoText")

    def init_bullet(self):

        # Create a collision shape and node for the camera
        camera_shape = BulletSphereShape(3)
        self.camera_node = BulletRigidBodyNode("Camera")
        self.camera_node.addShape(camera_shape)
        self.camera_node.setMass(1)
        self.camera_node.setDeactivationEnabled(False)

        # Attach the node to the render tree
        self.camera_np = self.base.render.attachNewNode(self.camera_node)
        self.camera_np.setCollideMask(BitMask32.bit(1))
        self.base.camera.reparentTo(self.camera_np)

        self.camera_node.setCcdMotionThreshold(0.01)
        self.camera_node.setCcdSweptSphereRadius(0.5)

        # Add the camera node to the Bullet world
        self.base.bullet_world.attachRigidBody(self.camera_node)

    def lock_mouse(self):
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_absolute)
        self.base.win.requestProperties(props)
        self.base.win.movePointer(0, self.base.win.getXSize() // 2, self.base.win.getYSize() // 2)

    def accept_inputs(self):
        self.base.accept("z", self.update_key_map, ["z", True])
        self.base.accept("z-up", self.update_key_map, ["z", False])
        self.base.accept("s", self.update_key_map, ["s", True])
        self.base.accept("s-up", self.update_key_map, ["s", False])
        self.base.accept("q", self.update_key_map, ["q", True])
        self.base.accept("q-up", self.update_key_map, ["q", False])
        self.base.accept("d", self.update_key_map, ["d", True])
        self.base.accept("d-up", self.update_key_map, ["d", False])
        self.base.accept("control", self.update_key_map, ["control", True])
        self.base.accept("control-up", self.update_key_map, ["control", False])
        self.base.accept("space", self.update_key_map, ["space", True])
        self.base.accept("space-up", self.update_key_map, ["space", False])

    def update_key_map(self, key, state):
        self.key_map[key] = state

    def update_camera(self, task):

        velocity = Vec3(0,0,self.camera_node.get_linear_velocity().z)

        if not self.paused:
            dt = globalClock.getDt()

            clone = self.camera_np.copyTo(self.base.render)
            clone.setHpr(self.h, 0, 0)

            forward = clone.getQuat().getForward() * self.speed * dt
            right = clone.getQuat().getRight() * self.speed * dt
            up = clone.getQuat().getUp() * self.speed * dt

            clone.removeNode()


            
            if self.key_map["z"]:
                velocity += forward
            if self.key_map["s"]:
                velocity -= forward
            if self.key_map["q"]:
                velocity -= right
            if self.key_map["d"]:
                velocity += right

            contact_under = False

            result = self.base.bullet_world.contactTest(self.camera_node)
            for contact in result.getContacts():
                point = contact.getManifoldPoint().getPositionWorldOnB()
                position = self.camera_np.getPos()
                if point[2] < position[2]:
                    contact_under = True

            if self.key_map["space"] and contact_under:
                print("Jumped")
                velocity += up
                
        self.camera_node.setLinearVelocity(velocity)

        return Task.cont

    def update_camera_direction(self, task):
        if self.base.mouseWatcherNode.hasMouse() and (not self.paused and not self.mouse_free):
            x = self.base.mouseWatcherNode.getMouseX()
            y = self.base.mouseWatcherNode.getMouseY()

            self.h = self.h - x * self.mouse_sensitivity
            self.p = self.p + y * self.mouse_sensitivity
            self.base.camera.setHpr(0, 0, 0)
            self.camera_np.setHpr(self.h, self.p, 0)
            self.camera_node.setAngularVelocity(Vec3(0, 0, 0))

            self.base.win.movePointer(0, self.base.win.getXSize() // 2, self.base.win.getYSize() // 2)

        return Task.cont

    def update_info_text(self, task):
        pos = self.camera_np.getPos()
        hpr = self.base.camera.getHpr()
        self.info_text.setText(
            f"Position: x={pos.x:.2f}, y={pos.y:.2f}, z={pos.z:.2f}\n"
            f"Direction: h={hpr.x:.2f}, p={hpr.y:.2f}, r={hpr.z:.2f}"
        )
        return Task.cont

    def pause(self):
        self.paused = True
        props = WindowProperties()
        props.setCursorHidden(not self.paused)
        self.base.win.requestProperties(props)

    def run(self):
        self.paused = False
        props = WindowProperties()
        props.setCursorHidden(not self.paused)
        self.base.win.requestProperties(props)

    def free_mouse(self):
        self.mouse_free = True
        props = WindowProperties()
        props.setCursorHidden(not self.mouse_free)
        self.base.win.requestProperties(props)

    def back_mouse(self):
        self.mouse_free = False 
        props = WindowProperties()
        props.setCursorHidden(not self.mouse_free)
        self.base.win.requestProperties(props)
