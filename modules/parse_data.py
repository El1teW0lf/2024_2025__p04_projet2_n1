import json
import os
from panda3d.core import NodePath, Point3, Vec3, Quat
from panda3d.core import Shader,LVecBase3f
from panda3d.core import CollisionNode, CollisionBox, CollisionPolygon, BitMask32, TransparencyAttrib, Point3
from panda3d.bullet import BulletTriangleMesh, BulletRigidBodyNode, BulletTriangleMeshShape, BulletBoxShape
from panda3d.bullet import BulletDebugNode
from panda3d.core import Loader, TransformState

def parse_json(path,render,loader,short_path,bullet_world):

    if not os.path.exists(os.path.join(path+"/data.json")):
        print(f"Error: File not found at {path}")
        return

    with open(os.path.join(path+"/data.json"), "r") as json_file:
        data = json.load(json_file)
        
    scene_root = NodePath("SceneRoot")
    scene_root.reparentTo(render)
    scale_factor = 10

    count = 0

    for i in data:
        try:
            model_path = os.path.join(short_path, i["model_path"])
            model = loader.loadModel(model_path)
            if model is None:
                print(f"Error: Model not found at {model_path}")
                continue

            model.reparentTo(scene_root)

            position = Vec3(-i["position"][0], i["position"][2], i["position"][1])
            size = Vec3(i["size"][0], i["size"][2], i["size"][1])
            orientation = Vec3(i["orientation"][0], i["orientation"][2], i["orientation"][1]+180)

            model.setPos(position * scale_factor)
            model.setScale(0.01 * scale_factor)
            model.setHpr(orientation)
            for child in model.find_all_matches('**/+CollisionNode'):
                child.show()

            texture_path = os.path.join(short_path, i["texture_path"])
            texture = loader.loadTexture(texture_path)
            if texture is None:
                print(f"Warning: Texture not found at {texture_path}")
                
            else:
                model.setTexture(texture, 1)
                model.setTwoSided(True)

            collistion_type = 2

            if model.getTightBounds() and collistion_type == 1 :

                min_point, max_point = model.getTightBounds()
                if min_point == max_point:
                    print(f"Skipping collider for {i['model_path']} due to invalid bounding box.")
                    continue

                center = (min_point + max_point) / 2
                dimensions = max_point - min_point
                dimensions = size*100

                print(dimensions)

                collision_box = CollisionBox(center, dimensions.x / 2, dimensions.y / 2, dimensions.z / 2)
                collision_node = CollisionNode(f"{i['model_path']}_collider")
                collision_node.addSolid(collision_box)

                collision_node.setIntoCollideMask(BitMask32.bit(1))
                collision_node_path = model.attachNewNode(collision_node)

                collision_node_path.show()
                collision_node_path.setTransparency(TransparencyAttrib.MAlpha)
                collision_node_path.setColor(1, 0, 0, 0.3) 

            elif collistion_type == 2:
                geom = model.findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
                mesh = BulletTriangleMesh()
                mesh.addGeom(geom)
                shape = BulletTriangleMeshShape(mesh, dynamic=False)

                body = BulletRigidBodyNode(f"{i['model_path']}_collider")
                bodyNP = render.attachNewNode(body)
                bodyNP.node().addShape(shape)
                bodyNP.node().setMass(0)
                bodyNP.setPos(Vec3(-i["position"][0], -i["position"][1], i["position"][2])*scale_factor)
                bodyNP.setHpr(Vec3(i["orientation"][0]+180, i["orientation"][1], i["orientation"][2]))
                bodyNP.setScale(1*scale_factor)
                bodyNP.setCollideMask(BitMask32.bit(1))
                bullet_world.attachRigidBody(bodyNP.node())


            shader = Shader.load(Shader.SLGLSL, "shaders/psx_vert.glsl", "shaders/psx_frag.glsl")
            if shader is None:
                print("Error: Shader failed to load")
                continue

            model.setShader(shader)
            model.setShaderInput("Jitter", 1)
            model.setShaderInput("FogColor", (0, 0, 0))
            model.setShaderInput("FogDensity", 0.0005)
            model.setShaderInput("PixelScale", 1.5)
            model.setShaderInput("ColorDepth", 12.0)
            model.setShaderInput("pixel_size", 0.1)

            count += 1
        except Exception as e:
            print(f"Error processing model {i['model_path']}: {e}")


        scene_root.setHpr(-90,-270, 90)

