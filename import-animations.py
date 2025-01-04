
############################

# mirroring code

# Author https://github.com/JayReigns/Mirror-Animation/blob/main/README.md

bl_info = {
    "name": "Mirror Animation",
    "author": "JayReigns",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "VIEW3D > Right Click",
    "description": "Mirror Animation action",
    "category": "Animation"
}

import bpy
from bpy.types import Operator
from bpy.props import EnumProperty


NEGATE_DATA_PATH_XAXIS = (
    ('location', 0),
    ('rotation_quaternion', 2),
    ('rotation_quaternion', 3),
    ('rotation_euler', 2),
    ('rotation_euler', 1), # armature space z axis is y
)

NEGATE_DATA_PATH_YAXIS = (
    ('location', 2), # in armature space y axis is z
    ('rotation_quaternion', 2),
    ('rotation_quaternion', 1),
    ('rotation_euler', 0),
    ('rotation_euler', 1), # armature space z axis is y
)


#########################################################################################
# Create Mirror Map
#########################################################################################


def difference(a, b):
    """Find difference in two strings to check if they are left and right"""
    import os
    common_prefix = os.path.commonprefix((a,b))
    common_suffix = os.path.commonprefix((a[::-1],b[::-1]))[::-1]
    
    # TODO: add checks incase of 'alc' and 'arc'
    #       check if difference is at start or end
    #       check if surrounds with punctuation or camelcase
    return a[len(common_prefix) : len(a)-len(common_suffix)], b[len(common_prefix) : len(b)-len(common_suffix)]

def lower_tuple(wl):
    return tuple(w.lower() for w in wl)

def create_mirror_map(names, patterns=None):
    
    mirror_map = {}

    if patterns == None:
        # Insert more default pattern if necessary
        patterns = (('l', 'r'), ('left', 'right'))
    
    # lower case and remove difference eg. remove 't' from 'Left', 'Right'
    patterns = tuple(lower_tuple(difference(*pattern)) for pattern in patterns)
    rpatterns = tuple(pattern[::-1] for pattern in patterns)

    for lname in names:
        for name in names:
            if lower_tuple(difference(lname, name)) in (*patterns, *rpatterns):
                rname = name
                mirror_map[lname] = rname
                break
    
    return mirror_map


#########################################################################################
# Mirror Action
#########################################################################################


def negate_fcurve(fcurve):
    for k in fcurve.keyframe_points:
        k.co[1] = -k.co[1]
        k.handle_left[1] = -k.handle_left[1]
        k.handle_right[1] = -k.handle_right[1]

def mirror_action(act, axis='X'):
    
    if not (act and act.fcurves):
        print("No Keyframes")
        return
    
    # create name map
    # strip attribute suffix eg. 'pose.bones["root"].location' -> 'pose.bones["root"]'
    bone_names = {fc.data_path.rsplit('.', 1)[0] for fc in act.fcurves if '.' in fc.data_path}
    mirror_map = create_mirror_map(bone_names)

    if axis == 'X':
        negate_data_path_tuples = NEGATE_DATA_PATH_XAXIS
    elif axis == 'Y':
        negate_data_path_tuples = NEGATE_DATA_PATH_YAXIS
    else:
        raise ValueError(f"Unsupported {axis=}")

    for fc in act.fcurves:
        data_path = fc.data_path
        array_index = fc.array_index

        # bone curves are 'pose.bones["root"].location'
        # objects curves are simply 'location'
        path, _dot, attribute = data_path.rpartition('.')
        
        # check if it is bone curve then flip data_path
        if path and (path in mirror_map):
            fc.data_path = "".join((mirror_map[path], _dot, attribute))
        
        if (attribute, array_index) in negate_data_path_tuples:
            negate_fcurve(fc)


#########################################################################################
# OPERATORS
#########################################################################################


class ANIM_OT_Mirror_Action(Operator):
    """Mirrors Currently assigned Action"""
    bl_idname = "aniim.mirror_action"
    bl_label = "Mirror Action"
    bl_options = {"REGISTER","UNDO"}

    axis : EnumProperty(
        name="Axis",
        description="Select mirror axis",
        default='X',
        items = (
            ('X', 'X', "X axis"),
            ('Y', 'Y', "Y axis"),
            ('XY', 'XY', "Both XY axes"),
            ('O', 'Original', "Original"),
        )
    )

    @classmethod
    def poll(cls, context):
        return context.active_object \
            # and context.active_object.animation_data \
            # and context.active_object.animation_data.action \
            # and context.active_object.animation_data.action.fcurves

    def execute(self, context):

        if not context.active_object.animation_data:
            self.report({"ERROR"}, "No Animation Data")
            return {'CANCELLED'}
        if not context.active_object.animation_data.action:
            self.report({"ERROR"}, "No Action assigned")
            return {'CANCELLED'}
        if not context.active_object.animation_data.action.fcurves:
            self.report({"ERROR"}, "No Keyframes")
            return {'CANCELLED'}
        
        if self.axis in ('X', 'Y'): 
            mirror_action(context.active_object.animation_data.action, axis=self.axis)
        if self.axis == 'XY':
            mirror_action(context.active_object.animation_data.action, axis='X')
            mirror_action(context.active_object.animation_data.action, axis='Y')
        # Skip 'O'; helps back and forth between poses
        
        self.report({"INFO"}, f"Action mirrorred on {self.axis}-axis!")
        return {'FINISHED'}


#########################################################################################
# REGISTER/UNREGISTER
#########################################################################################


classes = (
    ANIM_OT_Mirror_Action,
)

def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(ANIM_OT_Mirror_Action.bl_idname, icon='MOD_MIRROR')

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.append(menu_func)

def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_pose_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()


#####################################################

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


def mirror_actions():
	for action in bpy.data.actions:
		if action.name in animation_params:
			params = animation_params[action.name]
			if 'mirror' in params:
				mirror_name = params['mirror']
				if mirror_name != None:
					print('should mirror: ' + action.name + ', name should be = ' + mirror_name)
					action_copy = action.copy()
					action_copy.name = mirror_name
					mirror_action(action_copy)
					action_copy.use_fake_user = True



combined_filepath = '/home/brad/gamedev/mosttrusted/gameresources/animations/combined.blend'

root_source_armature = '/home/brad/gamedev/mosttrusted/gameresources/animations/armature.fbx'
animation_source_files = get_animation_files()
animation_params = {
	'sitting' : {
		'disable_root_motion' : False,
		'mirror' : 'sitting-mirror',
	},
	'walking' : {
		'mirror': 'walking-mirror',
	},
	'rifle-strafe' : {
		'mirror': 'rifle-strafe-mirror',
	},
    'grind' : {
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
mirror_actions()

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.outliner.orphans_purge()
bpy.ops.import_scene.fbx(filepath=root_source_armature)

bpy.ops.wm.save_as_mainfile(filepath=combined_filepath)

#exit(0)


