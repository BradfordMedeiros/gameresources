import bpy
import os

base_dir = bpy.path.abspath("/home/brad/gamedev/mosttrusted/gameresources/")

def is_subdirectory(base, target):
    base = os.path.abspath(base)
    target = os.path.abspath(target)
    return os.path.commonpath([base]) == os.path.commonpath([base, target])


def print_red(text):
    print("\033[31mError:  " + text + "\033[0m")

has_errors = False
for img in bpy.data.images:
    abs_path = bpy.path.abspath(img.filepath)  # Convert to absolute path
    if len(img.filepath) == 0:
        continue

    is_correct_path = is_subdirectory(base_dir, abs_path)
    if not is_correct_path :
        print_red("Incorrect path reference: [" + img.filepath + "], length =" + str(len(img.filepath)))
    else:
        print("checked: " + abs_path)

if has_errors:
    print_red("Invalid paths")
    exit(1)
