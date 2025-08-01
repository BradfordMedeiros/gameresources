import bpy
import sys
import os 

# https://docs.blender.org/api/current/bpy.ops.export_scene.html

output_file = sys.argv[6]
output_format = sys.argv[7]

output_folder = os.path.dirname(output_file)

os.makedirs(output_folder, exist_ok=True)

print("output format is: " + output_format)

export_fbx = True

def build_fbx():
  bpy.ops.export_scene.fbx(
    filepath=output_file, 
    axis_forward='-Z', 
    axis_up='Y', 
    apply_unit_scale=True,  
    apply_scale_options='FBX_SCALE_NONE',
    global_scale=0.01,   # see https://developer.blender.org/T70161
    add_leaf_bones=False
  )

def build_dae():
  bpy.ops.wm.collada_export(
    filepath=output_file, 
    export_global_forward_selection='-Z',
    export_global_up_selection='Y',  
  )  

def build_gltf():
  bpy.ops.export_scene.gltf(
    filepath=output_file, 
    export_format='GLTF_SEPARATE',
    export_nla_strips=True 
  )

format_to_build = {
  'fbx': build_fbx,
  'dae': build_dae,
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

def validate_model():
  mesh_obj = None
  for obj in bpy.data.objects:
    if obj.name == 'model':
      mesh_obj = obj

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

build()




