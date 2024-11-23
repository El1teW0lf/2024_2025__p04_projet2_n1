from scenes import TestWorld,MainMenu
from direct.showbase.ShowBase import ShowBase 
from modules import parse_json
from panda3d.bullet import BulletWorld
from panda3d.core import Vec3

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))
        self.ui = {}

    def startup(self):
        MainMenu(self,self.start_game)


    def start_game(self):
        TestWorld(self)

    def reset(self):
        self.clear_all_ui()
        self.render.getChildren().detach()
        self.camera.reparentTo(self.render)    


    def clear_all_ui(self):
        def recursive_destroy(element):
            if isinstance(element, dict):
                for key in element:
                    recursive_destroy(element[key])
            elif isinstance(element, list):
                for item in element:
                    recursive_destroy(item)
            elif hasattr(element, "destroy"):
                element.destroy()

        recursive_destroy(self.ui)
        self.ui = {}

if __name__ == "__main__":
    app = Main()
    app.startup()
    app.run()
