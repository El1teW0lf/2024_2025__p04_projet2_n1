import json
import os
from panda3d.core import NodePath, Point3, Vec3, Quat

def parse_json(path,render,loader,short_path):

    if not os.path.exists(os.path.join(path+"/data.json")):
        print(f"Error: File not found at {path}")
        return

    with open(os.path.join(path+"/data.json"), "r") as json_file:
        data = json.load(json_file)
        
    scene_root = NodePath("SceneRoot")
    scene_root.reparentTo(render)

    for i in data:
        model = loader.loadModel(os.path.join(short_path,i["model_path"].replace("/","\\")))
        model.reparentTo(scene_root)
        texture = loader.loadTexture(os.path.join(short_path,i["texture_path"].replace("/","\\")))
        model.setTexture(texture, 1)


    scene_root.setHpr(0, 90, 0)