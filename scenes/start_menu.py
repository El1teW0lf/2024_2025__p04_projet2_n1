from direct.gui.DirectGui import DirectButton, DirectLabel, DirectFrame, DGG
from panda3d.core import TextNode, NodePath, GeomNode, Plane, CardMaker
from panda3d.core import Texture, Vec3

class MainMenu():
    def __init__(self, base,launch_function):
        super().__init__()
        self.on_launch = launch_function
        self.main = base
        self.main.reset()
        self.main.disableMouse()
        self.size_factor = 265

        self.width = self.main.win.getXSize()
        self.height = self.main.win.getYSize()

        self.create_bg()
        self.create_buttons()

    def create_bg(self):

        cm = CardMaker("plane")


        cm.setFrame(-self.width / self.size_factor, self.width / self.size_factor, -self.height / self.size_factor, self.height / self.size_factor) 
        plane = self.main.render.attachNewNode(cm.generate())
        plane.setColor(1, 1, 1, 1)  

        texture = self.main.loader.loadTexture("ui/bg_green.png") 
        plane.setTexture(texture)

        
        plane.setPos(0, 10, 0)  
        plane.lookAt(self.main.camera)
        plane.setHpr(plane.getH() + 180, plane.getP(), plane.getR())

    def create_buttons(self):
        cm = CardMaker("plane")
        cm.setFrame(-273 / self.size_factor / 2, 273 / self.size_factor / 2, -81 / self.size_factor / 2, 81 / self.size_factor / 2) 
        plane = self.main.render.attachNewNode(cm.generate())
        plane.setColor(1, 1, 1, 1)  
        plane.setTag("UI", "start_play_button")

        texture = self.main.loader.loadTexture("ui/play_icon_text.png") 
        plane.setTexture(texture)
        plane.setPos(0, 7, 0)  
        plane.lookAt(self.main.camera)
        plane.setHpr(plane.getH() + 180, plane.getP(), plane.getR())
        plane.setPos(-2, 7, 0)  


        cm = CardMaker("plane")
        cm.setFrame(-437 / self.size_factor / 2, 437 / self.size_factor / 2, -81 / self.size_factor / 2, 81 / self.size_factor / 2) 
        plane = self.main.render.attachNewNode(cm.generate())
        plane.setColor(1, 1, 1, 1)  
        plane.setTag("UI", "start_play_button")

        texture = self.main.loader.loadTexture("ui/settings_icon_text.png") 
        plane.setTexture(texture)
        plane.setPos(0, 7, 0) 
        plane.lookAt(self.main.camera)
        plane.setHpr(plane.getH() + 180, plane.getP(), plane.getR())
        plane.setPos(-2, 7, -0.2)  


    def start_game(self):
        print("Start Game clicked!")
        self.on_launch()

    def show_settings(self):
        print("Settings clicked!")

    def quit_game(self):
        print("Quit clicked!")
        self.userExit()

