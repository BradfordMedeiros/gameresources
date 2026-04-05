import bpy
import sys
import os 
import math
import mathutils

# https://docs.blender.org/api/current/bpy.ops.export_scene.html

output_file = sys.argv[6]
output_format = sys.argv[7]
is_big = False
if len(sys.argv) >= 9:
  is_big = sys.argv[8] == "big"

output_folder = os.path.dirname(output_file)

os.makedirs(output_folder, exist_ok=True)

print("output format is: " + output_format)
print("is big: " + str(is_big))

def build_gltf():
  bpy.ops.export_scene.gltf(
    filepath=output_file, 
    export_format='GLTF_SEPARATE',
    export_nla_strips=True 
  )

format_to_build = {
  'gltf': build_gltf,
}


build = format_to_build[output_format]
assert(build != None)

def validate_uniform_transform(mesh_obj, error_text):
  if mesh_obj.location.x != 0 or mesh_obj.location.y != 0 or mesh_obj.location.z != 0:
    print(error_text + ": location must be (0,0,0) for model got: " + str(mesh_obj.location))
    exit(1)

  if mesh_obj.scale.x != 1 or mesh_obj.scale.y != 1 or mesh_obj.scale.z != 1:
    print(error_text + ": scale is not 1, must be (1,1,1) for for model got: " + str(mesh_obj.scale))
    exit(1)

  if mesh_obj.rotation_euler.x != 0 or mesh_obj.rotation_euler.y != 0 or mesh_obj.rotation_euler.z != 0:
    print(error_text + ": rotation must be (0, 0, 0) got: " + str(mesh_obj.rotation_euler))
    exit(1)


def get_model():
  mesh_obj = None
  for obj in bpy.data.objects:
    if obj.name == 'model':
      mesh_obj = obj
  return mesh_obj 

def validate_model():
  mesh_obj = get_model()
  if mesh_obj == None:
    print('did not find root model should be named "model"')
    exit(1)

  if mesh_obj and mesh_obj.parent != None:
    parent = mesh_obj.parent
    if parent.type != 'ARMATURE':
      print('obj named model is parented, this is supposed to be the root obj, or parented to an armature')
      exit(1)

  if mesh_obj:
    validate_uniform_transform(mesh_obj, "model obj")

def validate_armatures():
  for obj in bpy.data.objects:
    if obj.type == 'ARMATURE':
      validate_uniform_transform(obj, "armature obj")

validate_model()
validate_armatures()

# This is specifically for trenchbroom.  Scale it up and rotate 180 along z (up), this orients it correctly
if is_big:
    model = get_model()
    if model is None:
        print("Cannot find model to scale")
        exit(1)

    scale_factor = 10

    # Scale the root model directly (works in background mode)
    model.scale = (scale_factor, scale_factor, scale_factor)
    model.rotation_euler[0] = math.radians(0)
    model.rotation_euler[1] = math.radians(0)
    model.rotation_euler[2] = math.radians(180)

    # Optional: scale children meshes to match (if needed)
    for child in model.children_recursive:
        if child.type == 'MESH':
            child.scale = tuple(s*scale_factor for s in child.scale)

    print(f"Applied big scale ({scale_factor}x) to {model.name} and its children")

build()




