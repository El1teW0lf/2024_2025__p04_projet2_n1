from panda3d.core import loadPrcFileData, WindowProperties
from controller import FreeCameraController
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

        self.base = base

        self.base.reset()

        self.userExit = base.userExit

        self.base.disableMouse()

        self.bullet_world = self.base.bullet_world

        self.base.setBackgroundColor(0,0,0)

        self.camera = self.base.camera
        self.loader = self.base.loader
        self.render = self.base.render

        self.camera.setPos(0, 0, 0)
        self.camera.setHpr(0, 0, 0)

        self.controller = FreeCameraController(self.base)

        shape = BulletPlaneShape(Vec3(0, 0, 100), 0)

        body = BulletRigidBodyNode('Ground')
        bodyNP = self.render.attachNewNode(body)
        bodyNP.node().addShape(shape)
        bodyNP.node().setMass(0)
        bodyNP.setPos(0, 0, -10)
        bodyNP.setCollideMask(BitMask32.bit(1))
        self.bullet_world.attachRigidBody(bodyNP.node())

        script_directory = os.path.dirname(os.path.realpath(__file__))
        folder_path = os.path.join(script_directory, "test_scene_2")

        self.base.camLens.setFov(90)
        parse_json(folder_path, self.render, self.loader, "scenes/test_scene_2", self.bullet_world)

        props = WindowProperties()
        props.setFullscreen(True)
        #self.win.requestProperties(props)

        screen_aspect_ratio = self.base.win.getProperties().getXSize() / self.base.win.getProperties().getYSize()
        self.base.camLens.setAspectRatio(screen_aspect_ratio)

        self.menu = PauseMenu(self)

        debugNode = BulletDebugNode('Debug')
        debugNode.showWireframe(False)
        debugNode.showConstraints(False)
        debugNode.showBoundingBoxes(False)
        debugNode.showNormals(False)
        debugNP = self.render.attachNewNode(debugNode)
        debugNP.show()

        self.bullet_world.setDebugNode(debugNP.node())

        self.base.accept("escape", self.toggle_pause_menu)
        self.base.taskMgr.add(self.update, 'draw_debug_world')

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
