"""
This file configures:
   1. data directories (IMPLEMENTED)
   2. path to archive executables (NOT IMPLEMENTED)
   3. paths to mysql (NOT IMPLEMENTED)
   
   # variables imported to other modules from here:
   # PATH, MYSQL_PATH
   # variables with a '_' prefix should not be imported or used outside global_ini
"""
import configparser
import os
from os import path

# Transiton:
#   - must rename csv.full to csv
#   - use get_output_folder():
#   - move dtaa folder outside project folder

# This file is in subfolder of _PROJECT_ROOT_DIR, so do path.dirname() twice
_PROJECT_ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))

def get_absolute_path(user_path, root_path = _PROJECT_ROOT_DIR ):    
    """
    Adjusts <user_path> to project root directory <_PROJECT_ROOT_DIR> if <path> is relative.
    If <user_path,> is absolute path, returns itself.
    """
    if path.isabs(user_path):
        return user_path
    else:
        return path.join(root_path, user_path)

# Load user settings
config = configparser.ConfigParser()
config.read('../settings.cfg')


# Read the directories chosen by the user, adjusting them to the project root if necessary

_PUBLIC_DATA_FOLDER = get_absolute_path(
    config.get('data directories', 'public_data_folder', fallback='data.downloadable')
)

_PRIVATE_DATA_FOLDER = get_absolute_path(
    config.get('data directories', 'private_data_folder', fallback='data.private')
)

_OUTPUT_FOLDER = get_absolute_path(
    config.get('data directories', 'output_folder', fallback='output')
)

# Form directories
def _get_dir_structure(folder, form):
    return {
        'rar': path.join(folder, form, 'rarzip'),
        'dbf': path.join(folder, form, 'dbf' ),
        'csv': path.join(folder, form, 'csv'),
        'txt': path.join(folder, form, 'txt')
    }

def _get_public_dirs(form):
    return _get_dir_structure(_PUBLIC_DATA_FOLDER, form)

def _get_private_dirs(form):
    return _get_dir_structure(_PRIVATE_DATA_FOLDER, form)

def _get_global_dirs():
    return {
        'database': path.join(_PROJECT_ROOT_DIR, 'database', 'db_dump'),
        'alloc'   : path.join(_PROJECT_ROOT_DIR, 'database', 'alloc'  ),
        'tables'  : path.join(_PROJECT_ROOT_DIR, 'database', 'tables' ),
        'output'  : _OUTPUT_FOLDER
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

def get_global_folder(folder_tag):
    """
    Return absolute path to global folder with database files.
    """
    dir_list = _get_global_dirs()
    return dir_list[folder_tag]

def get_output_folder():
    """
    Returns 'output' folder used to write final files
    """   
    return get_global_folder("output")


def generate_all_folder_names():
    for frm in  ('101', '102'):
        yield _get_public_dirs(frm)
        yield _get_private_dirs(frm)
    yield _get_global_dirs()


def create_default_directories(verbose = False):
    """
    Creates the default directories required by the application. 
    Some directories can be configured by the user in <settings.cfg> 
    in the project root.
    """
    if verbose:
        print("Directories used:")
    
    for dir_ in generate_all_folder_names():
       os.makedirs(dir_, exist_ok=True) 
       if verbose:
            print(dir_)


############################## Executables directories [zip/rar path]
# todo: import paths from settings.cfg, if not supplied use PATH below
#       or try understand if it windows or linux and use different defaults if not in settings.cfg 
#       settings.cfg always overrides defaults

PATH = {
    'unrar': path.join(_PROJECT_ROOT_DIR, 'bin', 'unrar.exe'),
    'z7': path.join(_PROJECT_ROOT_DIR, 'bin', '7za')
}    

# 
# PATH = {'unrar': 'usr/bin/unrar'),
#           'z7': 'usr/bin/7z'}

############################## Executables directories [mysql]
# todo: import a list from from settings.cfg
# 
# MYSQL_PATH = [r'C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin', r'C:\MySQL\bin']
