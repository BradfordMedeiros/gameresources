import bpy
from pathlib import Path

def delete_unwanted_objects(objtypes):
  cameras = [camera for camera in bpy.context.scene.objects if camera.type in objtypes]
  for camera in cameras:
    bpy.data.objects.remove(camera, do_unlink=True)  

delete_unwanted_objects(['CAMERA', 'LIGHT', 'MESH'])

def filepath_for_model(model):
  modelname = model['shape'] + '_' + str(model['width']) + 'x' + str(model['height'])
  filepath = './' + modelname + '.blend'
  return filepath

models = [
  { 'shape' : 'block', 'width' : 2, 'height' : 2, 'uv-tiling' : [1, 1] },
]

for model in models:
  filepath = filepath_for_model(model)
  print ("filepath is: " + filepath)
  if Path(filepath).is_file():
    print("Warning file: " + filepath + " already exists, exiting without writing any files")
    exit(1)

for model in models:
  bpy.ops.wm.save_mainfile(filepath = filepath_for_model(model))





print("hello world")