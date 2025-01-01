"""
Process:
    root source armature should be a fbx file matching the other animation skeletons but w/o any animations
    add animations to the source files array as desired

    running this script will generate a new .blend file.  
    This .blend file will then contain a skeleton that you can copy/paste into a new blend file with the model
    
    make sure all transformations not applied to deltas.
    so transform expand panel, make sure all 1 scale, no rotation, no location.  check animations to make sure looks good
	
    that model can be scaled and whatnot just fine in edit mode -> add with automatic weights
"""

import bpy
import os
from pathlib import Path

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.outliner.orphans_purge()

def all_files(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def get_animation_files():
	animation_source_files = []
	for fullpath in all_files('./animations/actions'):
		action_name = Path(fullpath).stem
		animation_source_files.append({
			'name' : action_name,
			'file' : fullpath,
		})
	return animation_source_files


def load_scene(filepath):
	old_objs = set(bpy.context.scene.objects)
	bpy.ops.import_scene.fbx(filepath=filepath)
	imported_objs = set(bpy.context.scene.objects) - old_objs
	return imported_objs

def rename_obj_action(obj):
	if obj != None and obj.animation_data != None:
		action = obj.animation_data.action
		action.name = animation['name']

def disable_root_motion():
	for action in bpy.data.actions:
		fcurves = action.fcurves
		for channel in fcurves:
			channel_name = channel.data_path
			if ('mixamorig:Hips' in channel_name) and ('location' in channel_name):
				should_disable = True
				if action.name in animation_params:
					params = animation_params[action.name]
					if 'disable_root_motion' in params:
						should_disable = params['disable_root_motion'] != False
				
				if should_disable:
					channel.mute = True

combined_filepath = '/home/brad/gamedev/mosttrusted/gameresources/animations/combined.blend'

root_source_armature = '/home/brad/gamedev/mosttrusted/gameresources/animations/armature.fbx'
animation_source_files = get_animation_files()
animation_params = {
	'sitting' : {
		'disable_root_motion' : False,
	},
}

for animation in animation_source_files:
	if not os.path.exists(animation['file']):
		print('file does not exist: ' + animation['file'])
		exit(1)

for animation in animation_source_files: 
	# this has the side effect of keeping the actions
	file_path = animation['file']
	imported_objs = load_scene(file_path)
	for obj in imported_objs:
		rename_obj_action(obj)

disable_root_motion()

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.outliner.orphans_purge()
bpy.ops.import_scene.fbx(filepath=root_source_armature)

bpy.ops.wm.save_as_mainfile(filepath=combined_filepath)

exit(0)

