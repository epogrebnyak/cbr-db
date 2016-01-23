"""
This module is responsible for directory structure
for input and output files.
"""

import os

from .conf import settings
from .date_engine import get_current_year


# This file is in subfolder of _PROJECT_ROOT_DIR, so do path.dirname() twice
_PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def prepare_output_dir(path):
    """
    Creates output directory used to write final files.
    This function guarantees that directory exists and is writable.
    """
    if not os.path.isdir(path):
        os.makedirs(path)
    mode = os.stat(path).st_mode & 0o777
    new_mode = mode | 0o222  # must be writable by all
    if new_mode != mode:
        os.chmod(path, new_mode)
    return path


def get_database_folder(folder_tag):
    """
    Return absolute path to global folder with database files.
    """
    if folder_tag == 'database':
        folder_tag = 'db_dump'
    return os.path.join(_PROJECT_ROOT_DIR, 'database', folder_tag)


def _get_dir_structure(folder, form):
    return {
        'rar': os.path.join(folder, form, 'rarzip'),
        'dbf': os.path.join(folder, form, 'dbf' ),
        'csv': os.path.join(folder, form, 'csv'),
        'txt': os.path.join(folder, form, 'txt')
    }


def _get_private_dirs(form):
    return _get_dir_structure(settings.PRIVATE_DATA_FOLDER, form)


def get_public_data_folder(form, subfolder_tag):
    """
    Return absolute path to public data folder.
    """
    dir_list = _get_dir_structure(os.path.join(settings.DATA_DIR, 'downloadable'), form)
    return dir_list[subfolder_tag]

def get_private_data_folder(form, subfolder_tag):
    """
    Return absolute path to private data folder.
    """
    dir_list = _get_dir_structure(os.path.join(settings.DATA_DIR, 'private'), form)
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
        dir_ = os.path.normpath(os.path.join(main_folder, str(year)))
        if os.path.isdir(dir_):
            yield dir_, year


def get_db_dumpfile_path(db_name):
    """
    Returns the path to sql dump files, configured in DIRLIST in the
    global initialization module.
    """
    directory = get_database_folder('database')
    sql_filename = db_name + ".sql"
    path = os.path.join(directory, sql_filename).replace("\\", "/")
    return path


def get_sqldump_table_and_filename(form):
    """
    Returns (f101, f101.sql) for form 101, and similar output for other forms.
    Support function, it is not called directly from the interface.
    """
    table = 'f' + form
    file = table + ".sql"
    return table, file
