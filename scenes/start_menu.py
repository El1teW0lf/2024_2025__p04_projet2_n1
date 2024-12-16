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
from math import sin, radians
from panda3d.core import WindowProperties, TransparencyAttrib

class MainMenu():
    def __init__(self, base,launch_function):
        super().__init__()
        self.on_launch = launch_function
        self.main = base
        self.main.reset()
        self.main.disableMouse()
        self.size_factor = 265*1.2

        props = WindowProperties()
        props.setCursorHidden(True)
        self.main.win.requestProperties(props)

        self.width = self.main.win.getXSize()
        self.height = self.main.win.getYSize()
        self.bullet_world = self.main.bullet_world

        self.show_debug_collision = False

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(self.show_debug_collision)
        debugNode.showConstraints(self.show_debug_collision)
        debugNode.showBoundingBoxes(self.show_debug_collision)
        debugNode.showNormals(self.show_debug_collision)
        debugNP = self.main.render.attachNewNode(debugNode)
        debugNP.show()

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
        self.start_play_button = self.create_button("start_play_button", -1.45* 1.325, 6.75, 0.05, 280 / self.size_factor* 1.325, 90 / self.size_factor)
        self.start_settings_button = self.create_button("start_settings_button", -1.2* 1.325, 6.75, -0.4, 450 / self.size_factor* 1.325, 90 / self.size_factor)
        self.start_quit_button = self.create_button("start_quit_button", -1.45* 1.325, 6.75, -0.85, 280 / self.size_factor* 1.325, 90 / self.size_factor)
        self.start_logo = self.create_button("start_logo", -1.0, 6.75, 1, 760 / self.size_factor * 1.2 , 340 / self.size_factor)
        texture = self.main.loader.loadTexture("ui/nice_logo.png")
        texture.setMinfilter(Texture.FTLinear) 
        texture.setMagfilter(Texture.FTLinear)
        self.start_logo.setTexture(texture)
        self.start_logo.setColor(1, 1, 1, 1)  


        self.cursor_image = "ui\Cursors\Outline\Default\cursor_none.png" 
        self.clicked_cursor_image = "ui\Cursors\Outline\Default\door_enter.png"
        self.custom_cursor = DirectLabel(
            frameColor=(0, 0, 0, 0),
            image=self.cursor_image,
            image_scale=0.05
        )
        self.custom_cursor.setTransparency(TransparencyAttrib.M_alpha)

        self.angle = 0
        self.main.taskMgr.add(self.rotate_with_sine, "RotateWithSine")
        self.main.taskMgr.add(self.check_touched,"CheckMouseTouched")
        self.main.taskMgr.add(self.update_cursor, "UpdateCursorTask")

    def create_bg(self):

        cm = CardMaker("plane")


        cm.setFrame(-self.width / self.size_factor * 1.325, self.width / self.size_factor * 1.325, -self.height / self.size_factor, self.height / self.size_factor) 
        plane = self.main.render.attachNewNode(cm.generate())
        plane.setColor(1, 1, 1, 1)  

        texture = self.main.loader.loadTexture("ui/start_menu.png") 
        texture.setMinfilter(Texture.FTLinear) 
        texture.setMagfilter(Texture.FTLinear)
        plane.setTexture(texture)

        shader = Shader.load(Shader.SLGLSL, "shaders/psx_vert.glsl", "shaders/psx_frag.glsl")
        if shader is None:
            print("Error: Shader failed to load")
            

        plane.setShader(shader)
        plane.setShaderInput("Jitter", 2)
        plane.setShaderInput("FogColor", (0, 0, 0))
        plane.setShaderInput("FogDensity", 0.0005)
        plane.setShaderInput("PixelScale", 1)
        plane.setShaderInput("ColorDepth", 18.0)
        plane.setShaderInput("pixel_size", 0.1)

        
        plane.setPos(0, 7, 0)  
        plane.lookAt(self.main.camera)
        plane.setHpr(plane.getH() + 180, plane.getP(), plane.getR())

    def create_button(self,tag, x, y, z, size_x, size_y):
        cm = CardMaker("plane")
        cm.setFrame(-size_x / 2, size_x / 2, -size_y / 2, size_y / 2)
        plane = self.main.render.attachNewNode(cm.generate())
        plane.setColor(1, 1, 1, 1)
        plane.setTag("UI", tag)
        plane.setPos(0, 6.75, 0)
        plane.lookAt(self.main.camera)
        plane.setHpr(plane.getH() + 180, plane.getP(), plane.getR())
        plane.setPos(x, y, z)
        plane.setTransparency(TransparencyAttrib.MAlpha)
        plane.setColor(1, 1, 1, 0)

        # Add collision node
        collision_node = CollisionNode(f"{tag}_collider")
        collision_box = CollisionBox((0, 0, 0), size_x / 2, 0.1, size_y / 2)
        collision_node.addSolid(collision_box)
        collider = plane.attachNewNode(collision_node)

        #collider.show()

        self.collision_traverser.addCollider(collider, self.collision_handler)

        return plane

    def start_game(self):
        print("Start Game clicked!")
        self.on_launch()

    def show_settings(self):
        print("Settings clicked!")

    def quit_game(self):
        print("Quit clicked!")
        self.main.userExit()

    def handle_button_press(self,tag):
        if tag == "start_play_button":
            self.start_game()
        elif tag == "start_settings_button":
            self.show_settings()
        elif tag == "start_quit_button":
            self.quit_game()

    def check_touched(self,task):
        if self.main.mouseWatcherNode.hasMouse():
            mpos = self.main.mouseWatcherNode.getMouse()
            self.picker_ray.setFromLens(self.main.camNode, mpos.getX(), mpos.getY())

            self.collision_traverser.traverse(self.main.render)

            collided = False

            if self.collision_handler.getNumEntries() > 0:
                self.collision_handler.sortEntries()
                picked_obj = self.collision_handler.getEntry(0).getIntoNodePath()

                picked_obj = picked_obj.findNetTag("UI")
                if not picked_obj.isEmpty():
                    collided = True

            if collided:
                self.custom_cursor["image"] = self.clicked_cursor_image
            else:
                self.custom_cursor["image"] = self.cursor_image

        return task.cont
    def on_click(self):
        if self.main.mouseWatcherNode.hasMouse():
            mpos = self.main.mouseWatcherNode.getMouse()
            self.picker_ray.setFromLens(self.main.camNode, mpos.getX(), mpos.getY())

            self.collision_traverser.traverse(self.main.render)

            if self.collision_handler.getNumEntries() > 0:
                self.collision_handler.sortEntries()
                picked_obj = self.collision_handler.getEntry(0).getIntoNodePath()

                picked_obj = picked_obj.findNetTag("UI")
                if not picked_obj.isEmpty():
                    self.handle_button_press(picked_obj.getTag("UI"))
    

    def update_cursor(self,task):
        if self.main.mouseWatcherNode.hasMouse():
            mouse_x = self.main.mouseWatcherNode.getMouseX()* (16/8.8)
            mouse_y = self.main.mouseWatcherNode.getMouseY()
            self.custom_cursor.setPos(mouse_x, 0, mouse_y)
        return task.cont

    def rotate_with_sine(self, task):
        self.angle += 2
        if self.angle >= 360:
            self.angle = 0 

        sine_value = sin(radians(self.angle)) * 20 
        
        self.start_logo.setHpr(0, 0, sine_value)
        
        return task.cont
