#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
**Purpose**

This program serves as a quick replacement for the modules
'bulk_rename_index_main.py' and 'bulk_rename_index_exec.py', the latter of which
implements the funcionalities included in the former.

In order to keep it simple and fast, but readable and easily reusable,
no external modules have been imported. 
However, it is advisble to define custom functions.

You can restructure this file at your complete choice, such as recurse
into a directory and modify the file or directory renaming rules.
"""

#----------------#
# Import modules #
#----------------#

import os
from pathlib import Path

#------------------#
# Define functions #
#------------------#

def change_to_path_and_store(path_str):
    main_posix_path = Path(main_path)
    os.chdir(main_posix_path)
    
    
def get_current_path():
    cwd = Path.cwd()
    return cwd


def get_obj_list(main_posix_path, obj_type):    
    if obj_type not in obj_type_list:
        raise ValueError("You must choose between these object type options: "
                         f"{obj_type_list}.")
    else:
        obj_list = object_listing_dict.get(obj_type)(main_posix_path)
        obj_list.sort()
        return obj_list
     
    
def print_format_string(strin2format, arg_list):
    print(strin2format.format(*arg_list))

#-------------------#
# Define parameters #
#-------------------#

# Path objects #
#--------------#

# Define the main path #
main_path = "/home/jonander/Pictures/2022"

# Change to the desired directory and get that path #
change_to_path_and_store(main_path)
cwd = get_current_path()

# List of files (or directories) in that path #
obj_list = get_obj_list(cwd, "directory")
len_obj_list = len(obj_list)

# Progress information string #
rename_progress_info_str = """Current directory : {}
File or directory list : {}
Length of the list : {}
"""

# Switch case dictionaries #
#--------------------------#

# List of objects in a path or list of them #
obj_type_list = ["file" ,"directory"]

object_listing_dict = {
    obj_type_list[0] : lambda main_posix_path : [file.name
                                                 for file in main_posix_path.iterdir() 
                                                 if file.is_file()],
    obj_type_list[1] : lambda main_posix_path : [dirc.name 
                                                 for dirc in main_posix_path.iterdir() 
                                                 if dirc.is_dir()]
    }

#--------------------#
# Batch rename files #
#--------------------#

# Print basic information such as current path, list of files and its length #
arg_list = [cwd, obj_list, len_obj_list]
print_format_string(rename_progress_info_str, arg_list)

# Perform the file renaming #
for num, file in enumerate(obj_list, start=1):
    new_num = f"{num:02d}"
    ext = file.suffix
    new_file = f"{new_num}{ext}"
    
    print(file, new_file)
    # os.rename(f, new_file)