import json
import os
from panda3d.core import NodePath, Point3, Vec3, Quat
from panda3d.core import Shader,LVecBase3

def parse_json(path,render,loader,short_path,camera,camLens):

    if not os.path.exists(os.path.join(path+"/data.json")):
        print(f"Error: File not found at {path}")
        return

    with open(os.path.join(path+"/data.json"), "r") as json_file:
        data = json.load(json_file)
        
    scene_root = NodePath("SceneRoot")
    scene_root.reparentTo(render)

    count = 0

    for i in data:
        model = loader.loadModel(os.path.join(short_path,i["model_path"].replace("/","/")))
        model.reparentTo(scene_root)
        texture = loader.loadTexture(os.path.join(short_path,i["texture_path"].replace("/","/")))
        model.setTexture(texture, 1)
        model.setTwoSided(True)

        shader = Shader.load(Shader.SLGLSL, "shaders/psx_vert.glsl", "shaders/psx_frag.glsl")
        model.setShader(shader)

        model.setShaderInput("Jitter", 1)
        model.setShaderInput("FogColor", (0, 0, 0))  # RGB fog color
        model.setShaderInput("FogDensity", 0.0005)
        model.setShaderInput("PixelScale", 1.5)
        model.setShaderInput("ColorDepth", 12.0)
        model.setShaderInput("pixel_size", 0.1)

        count += 1


    scene_root.setHpr(90,180,0)

