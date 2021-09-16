import bpy

def delete_unwanted_objects(objtypes):
  cameras = [camera for camera in bpy.context.scene.objects if camera.type in objtypes]
  for camera in cameras:
    bpy.data.objects.remove(camera, do_unlink=True)  

def getfilename():
  filename = bpy.path.basename(bpy.context.blend_data.filepath)
  name = '.'.join(filename.split('.')[0:-1])  # get rid of .blend
  if len(name) <= 0:
    raise Exception("Cannot figure out filename")
  return name

delete_unwanted_objects(['CAMERA', 'LIGHT'])

if len(bpy.context.scene.objects) > 1:
  raise Exception("Cannot fix model automatically because more than one object in scene")

bpy.context.scene.objects[0].name = getfilename()
bpy.context.scene.objects[0].select_set(True)
bpy.ops.object.mode_set(mode="OBJECT")

# Modengine also no support transforms on root node, so this must be unit (and that's nicer)
result = bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
is_successful = 'FINISHED' in result
if not is_successful:
  raise Exception("Error applying root transform to model")

bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_mainfile()