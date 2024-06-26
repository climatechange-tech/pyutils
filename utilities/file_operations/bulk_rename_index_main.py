#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------#
# Import modules #
#----------------#

from pathlib import Path

#-----------------------#
# Import custom modules #
#-----------------------#

from pytools.arrays_and_lists.array_data_manipulation import select_array_elements
from pytools.files_and_directories import file_and_directory_handler, file_and_directory_paths
from pytools.parameters_and_constants import global_parameters
from pytools.time_handling.datetime_operators import get_current_datetime, get_obj_operation_datetime
from pytools.strings import information_output_formatters, string_handler
from pytools.utilities.introspection_utils import get_caller_method_all_args

# Create aliases #
#----------------#

rename_objects = file_and_directory_handler.rename_objects

find_all_file_extensions = file_and_directory_paths.find_all_file_extensions
find_files_by_ext = file_and_directory_paths.find_files_by_ext
find_files_by_globstr = file_and_directory_paths.find_files_by_globstr

find_all_directories = file_and_directory_paths.find_all_directories
find_file_containing_dirs_by_globstr = file_and_directory_paths.find_file_containing_dirs_by_globstr

basic_time_format_strs = global_parameters.basic_time_format_strs
basic_object_types = global_parameters.basic_object_types
non_std_time_format_strs = global_parameters.non_std_time_format_strs

format_string = information_output_formatters.format_string
print_format_string = information_output_formatters.print_format_string

find_substring_index = string_handler.find_substring_index
obj_path_specs = string_handler.obj_path_specs
modify_obj_specs = string_handler.modify_obj_specs

#------------------#
# Define functions #
#------------------#

def shorten_conflicting_obj_list():
    if not ((not isinstance(lcos_upper_limit, int) \
             and (isinstance(lcos_upper_limit, str) and lcos_upper_limit == 'inf'))\
            or (isinstance(lcos_upper_limit, int) and lcos_upper_limit >= 1)):
        
        raise ValueError("Limit of the number of conflicting files "
                         "to be written to an output file "
                         "must be an integer ranging from 1 to 'inf'.")
    else:
        if lcos_upper_limit == 'inf':
            return False
        else:
            return True


def loop_renamer(obj_list,
                 obj_type="file",
                 starting_number="default",  
                 zero_padding="default",
                 dry_run=False,
                 splitdelim=None):
    
    all_arg_names = list(get_caller_method_all_args().values())
    obj_type_arg_pos = find_substring_index(all_arg_names, "obj_type")
    
    if obj_type not in basic_object_types:
        raise ValueError("Unsupported object type "
                         f"(argument '{all_arg_names[obj_type_arg_pos]}'). "
                         f"Choose one from {basic_object_types}.")
        
    num_formatted_objs = []
    obj2change = obj2change_dict.get(obj_type)

    for obj_num, obj_name in enumerate(obj_list, start=starting_number):
        if zero_padding == "default":
            fpn_noext = obj_path_specs(obj_name, obj_spec_key="name_noext")
            new_zp = str(len(fpn_noext))
            num_format = f"{obj_num:0{new_zp}d}"    
        else:
            num_format = f"{obj_num:0{zero_padding}d}"    
            
        if obj_type == basic_object_types[0]:
            num_formatted_obj = modify_obj_specs(obj_name,
                                                 obj2change, 
                                                 num_format)
        else:
            fpn_parts = obj_path_specs(obj_name,
                                       obj_spec_key="name_noext_parts",
                                       splitdelim=splitdelim)
                    
            nf_changes_tuple = (fpn_parts[0], num_format)
            num_formatted_obj = modify_obj_specs(obj_name,
                                                   obj2change, 
                                                   nf_changes_tuple)
            
        if dry_run:
            num_formatted_objs.append(num_formatted_obj)
            
        else:
            rename_objects(obj_name, num_formatted_obj)
            
    lnffs = len(num_formatted_objs)
    
    if lnffs > 0:
        print("Dry-run mode chosen, "
              f"potentially renamed {obj_type} list will be given.")
        
        return num_formatted_objs
            

def loop_direct_renamer(obj_list, fixed_new_obj_list):  
    for obj, new_obj in zip(obj_list, fixed_new_obj_list):
        rename_objects(obj, new_obj)
        

def return_report_file_fixed_path(file_path_noname, 
                                  file_name,
                                  extension):
    
    report_file_path = f"{file_path_noname}/{file_name}.{extension}"
    return report_file_path


def reorder_objs(path,
                 obj_type,
                 extensions2skip="",
                 index_range="all",
                 starting_number="default",
                 zero_padding="default",
                 splitdelim=None):
    
    # Input parameter validation #
    all_arg_dict = get_caller_method_all_args()    
    all_arg_names = list(all_arg_dict.keys())
    defaults = list(all_arg_dict.values())
        
    zp_arg_pos = find_substring_index(all_arg_names, "zero_padding")
    start_num_arg_pos = find_substring_index(all_arg_names, "starting_number")
    ir_arg_pos = find_substring_index(all_arg_names, "index_range")
    
    if ((zero_padding != "default" and not isinstance(zero_padding, int))\
        or (zero_padding != "default"
            and isinstance(zero_padding, int) 
            and zero_padding < 1)):
        raise TypeError(f"Argument '{all_arg_names[zp_arg_pos]}' "
                        f"at position {zp_arg_pos} must either be "
                        "an integer equal or greater than 1.\n"
                        "Set to `None` if no zero padding is desired.")
          
    if path is None:
        raise ValueError("A path string or PosixPath must be given.")
        
    if (not isinstance(index_range, range)) or \
        (isinstance(index_range, str) and index_range != "all"):
        raise TypeError("Index range format must be of range(min, max). "
                        "Select 'all' if the whole available range "
                        "wants to be taken into account.")
    
    if obj_type == basic_object_types[0]:
        ext_list = find_all_file_extensions(extensions2skip, path, top_path_only=True)
        obj_list_uneven = find_files_by_ext(ext_list, path, top_path_only=True)
    
    elif obj_type == basic_object_types[1]:
        obj_list_uneven = find_all_directories(path, 
                                             top_path_only=True,
                                             include_root=True)
        
    lou = len(obj_list_uneven)
    
    if index_range == "all":
        
        """
        1st step
        --------
        
        Rename objects (files or directories) starting from the highest number,
        to prevent overwriting and object deletion because of
        unevenly spaced numbering.
        This operation guarantees monotonous and unity-increasing numbering.
        
        By default the program uses the length of the object list,
        but it can be change as needed.
        
        Due to irregular numbering 
        as a result of object copying or renaming from different devices,
        any numbered object can be larger than that length.
        Appart from that, there can be newer objects that contain characters
        and they even need to be placed back in the time.
        
        In order to prevent that problem, 
        the user can customize the starting number.
        
        In any case the program will firstly attempt a dry run and
        let know if there are conflicting objects.
        """
          
        if starting_number == "default":
            resetting_number = lou + 1
            
        else:
            """This option lets the user choose any starting number."""
            resetting_number = starting_number
            
        num_formatted_objs_dryRun_1 = loop_renamer(obj_list_uneven, 
                                                   starting_number=resetting_number,
                                                   zero_padding=zero_padding,
                                                   dry_run=True,
                                                   splitdelim=splitdelim)
                          
        """2nd step:
        Rename directories starting from 1, now that object numbering
        is evenly spaced.
        """
        
        num_formatted_objs_dryRun_2 = loop_renamer(num_formatted_objs_dryRun_1,
                                                   starting_number=1, 
                                                   zero_padding=zero_padding,
                                                   dry_run=True,
                                                   splitdelim=splitdelim)
                                        
        # Check for equally named, conflicting objects #
        #----------------------------------------------#
        
        if obj_type == basic_object_types[0]:
            conflicting_objs = [find_files_by_globstr(f"*{Path(nff_dR2).stem}*",
                                                      path,
                                                      top_path_only=True)
                                for nff_dR2 in num_formatted_objs_dryRun_2]
            
        elif obj_type == basic_object_types[1]:
            conflicting_objs = [find_file_containing_dirs_by_globstr(f"*{Path(nff_dR2).stem}*",
                                                            path,
                                                            top_path_only=True)
                                for nff_dR2 in num_formatted_objs_dryRun_2]
        
        lcos = len(conflicting_objs)
        
        if lcos > 0:
            
            # Set maximum length of the conflicting objects to write on file, if not 'inf'
            wantlimit = shorten_conflicting_obj_list()
            if wantlimit:
                conflicting_objs = conflicting_objs[:lcos_upper_limit]            
            
            report_file_name = report_filename_dict.get(obj_type)     
            report_file_path = return_report_file_fixed_path(path,
                                                             report_file_name,
                                                             fixed_ext)
            
            report_file_obj = open(report_file_path, "w")                    
         
            timestamp_str_objname_uneven\
            = get_obj_operation_datetime(obj_list_uneven,
                                         "modification", 
                                         time_format_str)
            
            timestamp_str_nff_dR2\
            = get_current_datetime(time_fmt_string=ctime_format_str)
            
            timestamp_str_confl_obj\
            = get_obj_operation_datetime(conflicting_objs,
                                         "modification", 
                                         time_format_str)
            
            for objname_uneven, nff_dR2, confl_obj in zip(obj_list_uneven,
                                                          num_formatted_objs_dryRun_2,
                                                          conflicting_objs):
            
                arg_tuple_reorder_objs1 = (objname_uneven, 
                                           timestamp_str_objname_uneven,
                                           nff_dR2,
                                           timestamp_str_nff_dR2,
                                           confl_obj, 
                                           timestamp_str_confl_obj)
                report_file_obj.write(format_string(conf_obj_info_str, arg_tuple_reorder_objs1))
                         
            report_file_obj.close()
                
            if obj_type == basic_object_types[0]:
                arg_tuple_reorder1 = ("files", report_file_name)
                print_format_string(conflicting_objects_warning, arg_tuple_reorder1)
                
            elif obj_type == basic_object_types[1]:
                arg_tuple_reorder2 = ("directories", report_file_name)
                print_format_string(conflicting_objects_warning, arg_tuple_reorder2) 
 
        else:
            
            report_file_name = "dry-run_renaming_report"    
            report_file_path = return_report_file_fixed_path(path,
                                                             report_file_name,
                                                             fixed_ext)
            report_file_obj = open(report_file_path, "w")                    
            
            for objname_uneven, nff_dR2 in zip(obj_list_uneven, num_formatted_objs_dryRun_2):
                arg_tuple_reorder_objs2 = (objname_uneven,
                                           timestamp_str_objname_uneven,
                                           nff_dR2,
                                           timestamp_str_nff_dR2)
                report_file_obj.write(conf_obj_info_str, arg_tuple_reorder_objs2)
                         
            report_file_obj.close()
                
            if obj_type == basic_object_types[0]:
                arg_tuple_reorder3 = ("files", report_file_name)
                print_format_string(no_conflicting_object_message, arg_tuple_reorder3)
                
            elif obj_type == basic_object_types[1]:
                arg_tuple_reorder4 = ("directories", report_file_name)
                print_format_string(no_conflicting_object_message, arg_tuple_reorder4)
                
            ansPerformChanges\
            = input("Would you like to perform the changes? [y/n] ")
 
            while (ansPerformChanges != "y" and ansPerformChanges != "n"):   
                ansPerformChanges\
                = input("Please write 'y' for 'yes' or 'n' for 'no' ")
                
            else:
                loop_direct_renamer(obj_list_uneven, num_formatted_objs_dryRun_2)
             
    else:
        
        obj_list_uneven_slice = select_array_elements(obj_list_uneven,
                                                      index_range)   
        
        if starting_number == "default":
            raise ValueError(f"'{all_arg_names[start_num_arg_pos]}' argument "
                             f"at position {start_num_arg_pos} "
                             f"cannot be '{defaults[start_num_arg_pos]}' "
                             f"if '{ir_arg_pos}' argument is not None")
               
        num_formatted_objs_dryRun = loop_renamer(obj_list_uneven_slice, 
                                                 starting_number=starting_number, 
                                                 zero_padding=zero_padding,
                                                 dry_run=True,
                                                 splitdelim=splitdelim)
          
        # Check for equally named, conflicting objects #
        #----------------------------------------------#
        
        if obj_type == basic_object_types[0]:
            conflicting_objs = [find_files_by_globstr(f"*{Path(nff_dR).stem}*",
                                                      path,
                                                      top_path_only=True)
                                for nff_dR in num_formatted_objs_dryRun]
        
        elif obj_type == basic_object_types[1]:
            conflicting_objs = [find_file_containing_dirs_by_globstr(f"*{Path(nff_dR).stem}*",
                                                            path,
                                                            top_path_only=True)
                                for nff_dR in num_formatted_objs_dryRun]
            
        lcos = len(conflicting_objs)
        
        if lcos > 0:
            
            # Set maximum length of the conflicting objects to write on file, if not 'inf'
            wantlimit = shorten_conflicting_obj_list()
            if wantlimit:
                conflicting_objs = conflicting_objs[:lcos_upper_limit]   
                
            report_file_name = report_filename_dict.get(obj_type)
            report_file_path = return_report_file_fixed_path(path,
                                                             report_file_name,
                                                             fixed_ext)
            
            report_file_obj = open(report_file_path, "w")                    
              
            timestamp_str_objname_unevens\
            = get_obj_operation_datetime(obj_list_uneven_slice,
                                         "modification", 
                                         time_format_str)
            
            timestamp_str_nff_dR\
            = get_current_datetime(time_fmt_string=ctime_format_str)
            
            timestamp_str_confl_obj\
            = get_obj_operation_datetime(conflicting_objs,
                                         "modification", 
                                         time_format_str)
            
            for objname_unevens, nff_dR, confl_obj in zip(obj_list_uneven_slice,
                                                          num_formatted_objs_dryRun,
                                                          conflicting_objs):
            
                arg_tuple_reorder_objs3 = (objname_unevens, 
                                           timestamp_str_objname_unevens,
                                           nff_dR,
                                           timestamp_str_nff_dR,
                                           confl_obj,
                                           timestamp_str_confl_obj)
                report_file_obj.write(format_string(conf_obj_info_str, arg_tuple_reorder_objs3))
                         
            report_file_obj.close()
                
            print(f"\n\nSome renamed objs conflict! Information is stored "
                  f"at file '{report_file_name}'.")
                
        else:
            
            report_file_name = "dry-run_renaming_report"    
            report_file_path = return_report_file_fixed_path(path,
                                                             report_file_name,
                                                             fixed_ext)
            report_file_obj = open(report_file_path, "w")                    
            
            for objname_unevens, nff_dr in zip(obj_list_uneven_slice, 
                                               num_formatted_objs_dryRun):
                arg_tuple_reorder_objs4 = (objname_unevens, nff_dR)
                report_file_obj.write(format_string(dry_run_info_str, arg_tuple_reorder_objs4))
                         
            report_file_obj.close()
                
            print("No conflicting objs found. "
                  "Please check the dry-run renaming information "
                  f"at file '{report_file_name}'.")
       
            ansPerformChanges\
            = input("Would you like to perform the changes? [y/n] ")
 
            while (ansPerformChanges != "y" and ansPerformChanges != "n"):
                ansPerformChanges\
                = input("Please write 'y' for 'yes' or 'n' for 'no' ")
            else:
                loop_direct_renamer(obj_list_uneven_slice, num_formatted_objs_dryRun)
                           

#--------------------------#
# Parameters and constants #
#--------------------------#

# Time formatting strings #
time_format_str = basic_time_format_strs["H"]
ctime_format_str = non_std_time_format_strs["CFT_H"]

# Fixed extension to reuse at different parts of the objname_unevennctions #
fixed_ext = "txt"

# Fixed length of the list containing the conflicting file or directory names #
"""Set the minimum limit to 1.
If no limit wants to be considered, set the parameter to 'inf'
"""
lcos_upper_limit = 2
        

# Preformatted strings #
#----------------------#

# Object path comparisons and conflicts, if any, due to already existing ones #
conf_obj_info_str\
= """'{}' <--> '{}' renamed to '{}' <--> '{}' conflicts with '{}' <--> '{}'\n"""

dry_run_info_str = """'{}' renamed to '{}'\n"""

conflicting_objects_warning = """\n\nSome renamed {} conflict!
Information is stored at file '{}'."""

no_conflicting_object_message = """No conflicting {} found
Please check the dry-run renaming information at file '{}'."""


# Switch case dictionaries #
#--------------------------#

report_filename_dict = {
    basic_object_types[0] : "conflicting_files_report",
    basic_object_types[1] : "conflicting_directories_report"
    }

obj2change_dict = {
    basic_object_types[0] : "name_noext",
    basic_object_types[1] : "name_noext_parts"
    }