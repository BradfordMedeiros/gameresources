
# exec(open('/home/brad/gamedev/mosttrusted/gameresources/scale-armature.py').read())


# This script scales a model while preserving the keyframe animations
# This -- ought -- to be built into blender, but it doesn't seem to be (bug?)

def scale_model(scale):
	bpy.data.objects['Armature'].scale.x = scale
	bpy.data.objects['Armature'].scale.y = scale
	bpy.data.objects['Armature'].scale.z = scale

	armature = bpy.data.objects['Armature']
	bpy.ops.object.select_all(action='DESELECT')
	armature.select_set(True)
	bpy.context.view_layer.objects.active = armature
	bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def update_keyframes(scale):
 	for action in bpy.data.actions:
 		curves = action.fcurves
 		for curve in curves:
 			keyframes = curve.keyframe_points
 			is_location_keyframe = 'location' in curve.data_path

 			print("is location = " + str(is_location_keyframe) + " " + curve.data_path)

 			if is_location_keyframe:
 				for keyframe in keyframes:
 					if curve.array_index == 0:
 						keyframe.co[1] *= scale[0]
 					elif curve.array_index == 1:
 						keyframe.co[1] *= scale[1]
 					elif curve.array_index == 2:
 						keyframe.co[1] *= scale[2]


def normalize_scale():
	scale_all(1)

def scale_all(relative_scale):
	scale_model(relative_scale)
	update_keyframes([relative_scale, relative_scale, relative_scale])

def scale_to_dim(height):
	old_height = bpy.data.objects['Armature'].dimensions.z
	relative_scale = height / old_height
	scale_all(relative_scale)

