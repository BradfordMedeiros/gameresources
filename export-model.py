import bpy
import sys
import os 

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
  )

format_to_build = {
  'fbx': build_fbx,
  'dae': build_dae,
  'gltf': build_gltf,
}


build = format_to_build[output_format]
assert(build != None)
build()




