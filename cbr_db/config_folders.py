"""
This file configures:
   1. data directories
   2. path to archive executables
   3. paths to mysql
   
   # variables imported to other modules from here:
   # PATH, MYSQL_PATH
   # variables with a '_' prefix should not be imported or used outside global_ini
"""
import os
from os import path

from .conf import settings
from .date_engine import get_current_year


# This file is in subfolder of _PROJECT_ROOT_DIR, so do path.dirname() twice
_PROJECT_ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))


# Form directories
def _get_dir_structure(folder, form):
    return {
        'rar': path.join(folder, form, 'rarzip'),
        'dbf': path.join(folder, form, 'dbf' ),
        'csv': path.join(folder, form, 'csv'),
        'txt': path.join(folder, form, 'txt')
    }

def _get_public_dirs(form):
    return _get_dir_structure(settings.PUBLIC_DATA_FOLDER, form)

def _get_private_dirs(form):
    return _get_dir_structure(settings.PRIVATE_DATA_FOLDER, form)

def _get_global_dirs():
    return {
        'database': path.join(_PROJECT_ROOT_DIR, 'database', 'db_dump'),
        'alloc'   : path.join(_PROJECT_ROOT_DIR, 'database', 'alloc'  ),
        'tables'  : path.join(_PROJECT_ROOT_DIR, 'database', 'tables' ),
        'output'  : settings.OUTPUT_FOLDER
    }

def get_public_data_folder(form, subfolder_tag):
    """
    Return absolute path to public data folder.
    """
    dir_list = _get_public_dirs(form)
    return dir_list[subfolder_tag]

def get_private_data_folder(form, subfolder_tag):
    """
    Return absolute path to private data folder.
    """
    dir_list = _get_private_dirs(form)
    return dir_list[subfolder_tag]
    
def generate_private_data_annual_subfolders(form, subfolder_tag='txt'):
    """
    Will return paths 2015
        D:\git\cbr-data\data.private\101\txt\2004
        ...
        D:\git\cbr-data\data.private\101\txt\2015
    
    """
    for year in range(2004, get_current_year()+1):        
        main_folder = get_private_data_folder(form, subfolder_tag)
        dir_ = os.path.normpath(
                                os.path.join(main_folder,str(year))
                                )
        # print(dir_)
        if os.path.isdir(dir_):
            print("Exists:" + dir_)
            yield dir_, year    
            

def get_global_folder(folder_tag):
    """
    Return absolute path to global folder with database files.
    """
    dir_list = _get_global_dirs()
    return dir_list[folder_tag]

def get_output_folder():
    """
    Returns 'output' folder used to write final files.
    This function guarantees that folder exists and is writable.
    """   
    path = get_global_folder("output")
    if not os.path.isdir(path):
        os.makedirs(path)
    mode = os.stat(path).st_mode & 0o777
    new_mode = mode | 0o222  # must be writable by all
    if new_mode != mode:
        os.chmod(path, new_mode)
    return path
