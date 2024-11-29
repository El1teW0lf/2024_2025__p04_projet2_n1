from panda3d.core import loadPrcFileData, WindowProperties
from controller import FreeCameraController,PlayerController
from modules import parse_json
import os
from menus import PauseMenu
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape, BulletRigidBodyNode
from panda3d.core import Vec3,BitMask32
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletBoxShape

configVars = """
win-size 1280 720
show-frame-rate-meter 1
"""
loadPrcFileData("", configVars)
loadPrcFileData("", "gl-version 3 2")


class TestWorld():
    def __init__(self,base):

        self.main = base

        self.main.reset()

        self.userExit = base.userExit

        self.main.disableMouse()

        self.bullet_world = self.main.bullet_world

        self.main.setBackgroundColor(0,0,0)

        self.camera = self.main.camera
        self.loader = self.main.loader
        self.render = self.main.render

        self.camera.setPos(0, 0, 0)
        self.camera.setHpr(0, 0, 0)

        self.controller = PlayerController(self.main)

        shape = BulletPlaneShape(Vec3(0, 0, 100), 0)

        body = BulletRigidBodyNode('Ground')
        bodyNP = self.render.attachNewNode(body)
        bodyNP.node().addShape(shape)
        bodyNP.node().setMass(0)
        bodyNP.setPos(0, 0, 0)
        bodyNP.setCollideMask(BitMask32.bit(1))
        self.bullet_world.attachRigidBody(bodyNP.node())

        script_directory = os.path.dirname(os.path.realpath(__file__))
        folder_path = os.path.join(script_directory, "test_scene_2")

        self.main.camLens.setFov(90)
        parse_json(folder_path, self.render, self.loader, "scenes/test_scene_2", self.bullet_world)

        props = WindowProperties()
        props.setFullscreen(True)
        #self.win.requestProperties(props)

        screen_aspect_ratio = self.main.win.getProperties().getXSize() / self.main.win.getProperties().getYSize()
        self.main.camLens.setAspectRatio(screen_aspect_ratio)

        self.menu = PauseMenu(self)

        self.show_debug_collision = False

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(self.show_debug_collision)
        debugNode.showConstraints(self.show_debug_collision)
        debugNode.showBoundingBoxes(self.show_debug_collision)
        debugNode.showNormals(self.show_debug_collision)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()

        self.bullet_world.setDebugNode(debugNP.node())

        self.main.accept("escape", self.toggle_pause_menu)
        self.main.taskMgr.add(self.update, 'draw_debug_world')

    def toggle_pause_menu(self):
        if self.menu.menu_frame.isHidden():
            self.controller.pause()
            self.menu.show()
        else:
            self.menu.hide()
            self.controller.run()

    def update(self,task):
        self.bullet_world.doPhysics(globalClock.getDt())
        return task.cont

if __name__ == "__main__":
    app = TestWorld()
    app.run()
