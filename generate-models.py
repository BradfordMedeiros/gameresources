import bpy
from pathlib import Path

from math import cos, sin, radians

models = [
  { 'shape' : 'block', 'width' : 1, 'height' : 1,  'depth' : 1 },
  { 'shape' : 'block', 'width' : 2, 'height' : 10,  'depth' : 0.5 },
  { 'shape' : 'plane', 'width' : 2, 'height' : 2 },
  { 'shape' : 'ramp', 'width' : 2, 'height' : 2, 'depth' : 1 },
  { 'shape' : 'ring', 'depth' : 1, 'resolution': 10, 'radius' : 1, 'hole-radius' : 0.5},

]

def delete_unwanted_objects(objtypes):
  cameras = [camera for camera in bpy.context.scene.objects if camera.type in objtypes]
  for camera in cameras:
    bpy.data.objects.remove(camera, do_unlink=True)  


def filepath_for_model(model):
  modelname = model['shape'] + '_' 

  if 'width' in model:
    modelname = modelname + 'x' + str(model['width']) 
  if 'height' in model:
    modelname = modelname + 'x' + str(model['height'])
  if 'depth' in model:
    modelname = modelname + 'x' + str(model['depth'])
  if 'radius' in model:
    modelname = modelname + 'r' + str(model['radius'])
  if 'hole-radius' in model:
    modelname = modelname + 'hr' + str(model['hole-radius'])
  if 'resolution' in model:
    modelname = modelname + 'res' + str(model['resolution'])
    
  filepath = './generated/' + modelname + '.blend'
  return filepath



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
  new_uv = bpy.context.active_object.data.uv_layers.new(name='NewUV')
 
  for loop in bpy.context.active_object.data.loops:
      new_uv.data[loop.index].uv = uv_coords[loop.index]


def create_plane(width, height):
  scale_width= 0.5 * width
  scale_height = 0.5 * height
  vertices = [(-scale_width, -scale_height, 0), (-scale_width, scale_height, 0), (scale_width, -scale_height, 0), (scale_width, scale_height, 0)]
  faces = [ (0, 1, 2), (2, 1, 3)]
  uv_coords = [(0, 0), (0, 1), (1, 0), (1, 0), (0, 1), (1, 1)]
  create_object(vertices, faces, uv_coords)

def create_block(width, height, depth):
  scale_width= 0.5 * width
  scale_height = 0.5 * height
  scale_depth = 0.5 * depth
  vertices = [
    (-scale_width, -scale_height, -scale_depth), (-scale_width, scale_height, -scale_depth), (scale_width, -scale_height, -scale_depth), (scale_width, scale_height, -scale_depth),  # front face
    (-scale_width, -scale_height, scale_depth), (-scale_width, scale_height, scale_depth), (scale_width, -scale_height, scale_depth), (scale_width, scale_height, scale_depth),  # back face
  ]
  faces = [ 
    (0, 1, 2), (2, 1, 3),           # front face   good 
    (6, 7, 4), (4, 7, 5),          # back face     good 
    (4, 5, 1), (0, 4, 1),          # left face  good
    (2, 3, 6), (6, 3, 7),          # right face good
    (1, 5, 3), (3, 5, 7),          # top face        good 
    (0, 2, 4),  (2, 6, 4),         # bottom face  good
  ]
  uv_coords = [
    (0, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (-1, 1),    # front face
    (0, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (-1, 1),    # back face
    (0, 0), (0, 1), (-1, 1), (-1, 0), (0, 0), (-1, 1),    # left face 
    (0, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (-1, 1),    # right face    (-1, 0), (0, 1), (-1, 1),    # right face   
    (0, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (-1, 1),    # top face
    (0, 0), (1, 0), (0, 1), (1, 0), (1, 1) , (0, 1),     # bottom face
  ]  
  create_object(vertices, faces, uv_coords)


def create_ramp(width, height, depth):
  scale_width= 0.5 * width
  scale_height = 0.5 * height
  scale_depth = 0.5 * depth
  vertices = [
    (-scale_width, -scale_height, -scale_depth), (-scale_width, scale_height, -scale_depth), (scale_width, -scale_height, -scale_depth), (scale_width, scale_height, -scale_depth),  # front face
    (-scale_width, -scale_height, scale_depth), (-scale_width, scale_height, scale_depth), (scale_width, -scale_height, scale_depth), (scale_width, scale_height, scale_depth),  # back face
  ]
  faces = [ 
    (0, 1, 2), (2, 1, 3),           # front face   good 
    (0, 4, 1),          # left face  good
    (2, 3, 6),        # right face good
    (0, 2, 4), (2, 6, 4),         # bottom face  good
    (6, 3, 1), (1, 4, 6)
  ]
  uv_coords = [
    (0, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (-1, 1),    # front face
    (-1, 0), (0, 0), (-1, 1),    # left face 
    (0, 0), (0, 1), (-1, 0),    # right face    (-1, 0), (0, 1), (-1, 1),    # right face   
    (0, 0), (1, 0), (0, 1), (1, 0), (1, 1) , (0, 1),     # bottom face
    (0, 0), (0, 1), (1, 1), (1, 1), (1, 0) , (0, 0),     # main ramp face
  ]  
  create_object(vertices, faces, uv_coords)


def connect_vertices(_faces, _uv_coords, vertex_index_from, vertex_index_to, size, flip_winding):
  for i in range(size):
    vertexFromPlus1 = vertex_index_from + 1 + i
    if vertexFromPlus1 == (vertex_index_from + size):
      vertexFromPlus1 = vertex_index_from

    vertexToPlus1 = vertex_index_to + 1 + i
    if vertexToPlus1 == (vertex_index_to + size):
      vertexToPlus1 = vertex_index_to

    face1 = None
    face2 = None
    if not flip_winding:
      face1 = (vertex_index_from + i, vertex_index_to + i, vertexFromPlus1)
      face2 = (vertexFromPlus1, vertex_index_to + i , vertexToPlus1)
    else:
      face1 = (vertexFromPlus1, vertex_index_to + i, vertex_index_from + i)
      face2 = (vertexToPlus1, vertex_index_to + i , vertexFromPlus1)


    _faces.append(face1)  # bottom right
    _faces.append(face2)  # top left

    # this just assumed the coords are square, which isn't actually right. 
    # Eg the main faces on the ring end up warped.  
    # Could look at each two triangle pair, calculate min and max, and then calculate uvs from that.  
    # also looks like some end up rotated 90 based on winding? maybe?
    if not flip_winding:
      _uv_coords.append((0, 1))
      _uv_coords.append((1, 1))
      _uv_coords.append((0, 0))

      _uv_coords.append((0, 0))
      _uv_coords.append((1, 1))
      _uv_coords.append((1, 0))
  
    else:
      _uv_coords.append((0, 0))
      _uv_coords.append((1, 1))
      _uv_coords.append((1, 0))
  
      _uv_coords.append((0, 1))
      _uv_coords.append((1, 1))
      _uv_coords.append((0, 0))



def create_plane_circle(_vertices, _faces, _uv_coords, resolution, radius, depth, flip_winding):
  initial_vertex_index = len(_vertices)

  halfDepth = 0.5 * depth
  for i in range(resolution):
    angle_radians = radians(i * (360 / resolution))
    x_value = radius * cos(angle_radians)
    z_value = radius * sin(angle_radians)
    _vertices.append((x_value, -halfDepth, z_value))

  for i in range(resolution):
    angle_radians = radians(i * (360 / resolution))
    x_value = radius * cos(angle_radians)
    z_value = radius * sin(angle_radians)
    _vertices.append((x_value, halfDepth, z_value))

  connect_vertices(_faces, _uv_coords, initial_vertex_index, initial_vertex_index + resolution, resolution, flip_winding)


def create_ring(depth, radius, hole_radius, resolution):
  vertices = []
  faces = []
  uv_coords = []  
  create_plane_circle(vertices, faces, uv_coords, resolution, hole_radius, depth, True)
  create_plane_circle(vertices, faces, uv_coords, resolution, radius, depth, False)

  connect_vertices(faces, uv_coords, 0, resolution * 2, resolution, False)  # 10 faces, so adds 20 faces
  connect_vertices(faces, uv_coords, resolution, resolution * 2 + resolution, resolution, True)  # 10 faces, so adds 20 faces  
  create_object(vertices, faces, uv_coords)

#for model in models:
#  filepath = filepath_for_model(model)
#  print ("filepath is: " + filepath)
#  if Path(filepath).is_file():
#    print("Warning file: " + filepath + " already exists, exiting without writing any files")
#    exit(1)

for model in models:
  delete_unwanted_objects(['CAMERA', 'LIGHT', 'MESH'])
  filepath = filepath_for_model(model)

  shape = model['shape'];
  if shape == 'block':
    width = model['width']
    height = model['height']
    depth = model['depth']
    create_block(width, height, depth)
  elif shape == 'plane':
    width = model['width']
    height = model['height']
    create_plane(width, height)
  elif shape == 'ramp':
    width = model['width']
    height = model['height']
    depth = model['depth']
    create_ramp(width, height, depth)
  elif shape == 'ring':
    depth = model['depth']
    radius = model['radius']
    hole_radius = model['hole-radius'];
    resolution = model['resolution'];
    create_ring(depth, radius, hole_radius, resolution) 
  else:
    print('invalid shape type: ' + shape)
    exit(1)

  bpy.ops.wm.save_mainfile(filepath = filepath)


