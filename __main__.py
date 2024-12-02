from scenes import TestWorld,MainMenu
from direct.showbase.ShowBase import ShowBase 
from modules import parse_json
from panda3d.bullet import BulletWorld
from panda3d.core import Vec3, WindowProperties
import line_profiler

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.bullet_world = BulletWorld()
        self.bullet_world.setGravity(Vec3(0, 0, -9.81))
        self.ui = {}
        self.keys = {}
        props = WindowProperties()
        props.setFullscreen(True)
        self.win.requestProperties(props)

        self.possible_keys = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", "{", "}", ";", ":", "'", '"', ",", ".", "<", ">", "/", "?", "\\", "|",
            "space", "tab", "enter", "backspace", "escape", "delete", "insert", "home", "end", "page_up", "page_down",
            "arrow_left", "arrow_right", "arrow_up", "arrow_down",
            "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",

        ]


        for key in self.possible_keys:  
            self.accept(key, self.on_key_press, [key])
            self.accept(key+ "-up", self.on_key_press , [key+ "-up"])
            self.accept(key+ "-repeat", self.on_key_press , [key+ "-repeat"])



    def startup(self):
        MainMenu(self,self.start_game)


    def start_game(self):
        TestWorld(self)

    def reset(self):
        self.clear_all_ui()
        self.render.getChildren().detach()
        self.camera.reparentTo(self.render)    

    def add_key(self,key,function,args):
        if key in self.keys:
            self.keys[key].append([function,args])
        else:
            self.keys[key] = [[function,args]]

    def add_any_key(self,function):
        for key in self.possible_keys:
            if key in self.keys:
                self.keys[key].append([function,key])
            else:
                self.keys[key] = [[function,key]]

    def on_key_press(self,key):
        if key in self.keys:
            for stuff in self.keys[key]:
                try:
                    if isinstance(stuff[1],list):
                        stuff[0](*stuff[1])
                    else:
                        stuff[0](stuff[1])
                except Exception as e:
                    print(f"Failed to run key press {key} on function {stuff} because of error {e}")

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
