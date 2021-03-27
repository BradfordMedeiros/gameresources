#!/usr/bin/env bash
import bpy
import sys
import os 

build_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "build")

axis_forward='-Z'
axis_up='Y'

model_to_build = sys.argv[6]
output_file = os.path.join(build_dir, model_to_build)
output_folder = os.path.dirname(output_file)

os.makedirs(output_folder, exist_ok=True)
bpy.ops.export_scene.fbx(filepath=output_file, axis_forward=axis_forward, axis_up=axis_up)