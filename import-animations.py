"""
Process:
    root source armature should be a fbx file matching the other animation skeletons but w/o any animations
    add animations to the source files array as desired

    running this script will generate a new .blend file.  
    This .blend file will then contain a skeleton that you can copy/paste into a new blend file with the model
    that model can be scaled and whatnot just fine in edit mode -> add with automatic weights

"""

import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.outliner.orphans_purge()

root_source_armature = "/home/brad/gamedev/mosttrusted/gameresources/animations/armature.fbx"

animation_source_files = [
	{ 'name' : 'jump', 'file' : "/home/brad/gamedev/mosttrusted/gameresources/animations/Jumping.fbx" },
	{ 'name' : 'run',  'file' : "/home/brad/gamedev/mosttrusted/gameresources/animations/Running.fbx" },
	{ 'name' : 'dance',  'file' : "/home/brad/gamedev/mosttrusted/gameresources/animations/hiphop_dance.fbx" },
]


def load_scene(filepath):
	old_objs = set(bpy.context.scene.objects)
	bpy.ops.import_scene.fbx(filepath=filepath)
	imported_objs = set(bpy.context.scene.objects) - old_objs
	return imported_objs

for animation in animation_source_files: 
	# this has the side effect of keeping the actions
	imported_objs = load_scene(animation['file'])
	for obj in imported_objs:
		if obj != None and obj.animation_data != None:
			action = obj.animation_data.action
			action.name = animation['name']
			print (action.name)
	
		

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.outliner.orphans_purge()
bpy.ops.import_scene.fbx(filepath=root_source_armature)

#exit(0)
