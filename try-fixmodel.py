import bpy

def delete_unwanted_objects(objtypes):
  cameras = [camera for camera in bpy.context.scene.objects if camera.type in objtypes]
  for camera in cameras:
    bpy.data.objects.remove(camera, do_unlink=True)  


delete_unwanted_objects(['CAMERA', 'LIGHT'])
bpy.ops.file.make_paths_relative()

bpy.ops.wm.save_mainfile()