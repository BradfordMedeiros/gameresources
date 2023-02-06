import bpy
from pathlib import Path

def delete_unwanted_objects(objtypes):
  cameras = [camera for camera in bpy.context.scene.objects if camera.type in objtypes]
  for camera in cameras:
    bpy.data.objects.remove(camera, do_unlink=True)  

delete_unwanted_objects(['CAMERA', 'LIGHT', 'MESH'])

def filepath_for_model(model):
  modelname = model['shape'] + '_' + str(model['width']) + 'x' + str(model['height'])
  filepath = './generated/' + modelname + '.blend'
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


# https://b3d.interplanety.org/en/how-to-create-a-new-mesh-uv-with-the-blender-python-api/

def create_object(vertices, faces, uv_coords):
  edges = []
  new_mesh = bpy.data.meshes.new('new_mesh')
  new_mesh.from_pydata(vertices, edges, faces)
  new_mesh.update()
  new_object = bpy.data.objects.new('new_object', new_mesh)

  new_collection = bpy.data.collections.new('new_collection')
  bpy.context.scene.collection.children.link(new_collection)

  new_collection.objects.link(new_object)
  bpy.context.scene.objects[0].name = "testobject"
  bpy.context.scene.objects[0].select_set(True)
  bpy.context.view_layer.objects.active = bpy.context.scene.objects[0]
  newuv = bpy.context.active_object.data.uv_layers.new(name='newuv')
 
  for loop in bpy.context.active_object.data.loops:
      new_uv.data[loop.index].uv = uv_coords[loop.index]


def create_block(width, height):
  vertices = [(-0.5, -0.5, 0), (-0.5, 0.5, 0), (0.5, -0.5, 0), (0.5, 0.5, 0)]
  faces = [ (0, 1, 2), (2, 1, 3)]
  uv_coords = [(0.375, 0.0), (0.625, 0.0), (0.625, 0.25)]
  create_object(vertices, faces, uv_coords)

create_block(2, 3)

for model in models:
  bpy.ops.wm.save_mainfile(filepath = filepath_for_model(model))





print("hello world")