import configparser
import os
from os import path

# variables imported to other modules from here:
# PATH, DB_NAMES, FORM_DATA, MYSQL_PATH
# variables with a '_' prefix should not be imported or used outside global_ini

# this global_ini.py file is in subfolder of DIR_ROOT, do path.dirname() twice
_DIR_ROOT = path.dirname(path.dirname(path.abspath(__file__)))

#############################################################################
# User settings - directories
#############################################################################

def make_prefix(PATH):
    """
    Returns a path relative to the project root if <PATH> is relative. If not,
    returns an absolute path.
    """
    if path.isabs(PATH):
        return PATH
    else:
        return path.join(_DIR_ROOT, PATH)

# load user settings
config = configparser.ConfigParser()
config.read('../settings.cfg')

# read the directories chosen by the user, adjusting them to the project root
# if necessary

_PUBLIC_DATA_FOLDER = make_prefix(
    config.get('directories', 'public_data_folder', fallback='data.downloadable')
)

_PRIVATE_DATA_FOLDER = make_prefix(
    config.get('directories', 'private_data_folder', fallback='data.private')
)

_OUTPUT_FOLDER = make_prefix(
    config.get('directories', 'output_folder', fallback='output')
)

#############################################################################
# 0. EXECUTABLES
#############################################################################

# Executables directories
PATH = {
    'unrar': path.join(_DIR_ROOT, 'bin', 'unrar.exe'),
    'z7': path.join(_DIR_ROOT, 'bin', '7za')
}

#############################################################################
# 1. DATA DIRECTORIES
#############################################################################

# form directories
def get_form_dirs(form):
    return {
        'rar': path.join(_PUBLIC_DATA_FOLDER, form, 'rarzip'  ),
        'dbf': path.join(_PUBLIC_DATA_FOLDER, form, 'dbf'     ),
        'csv': path.join(_PUBLIC_DATA_FOLDER, form, 'csv.full'),
        'output': _OUTPUT_FOLDER
    }

# Private data directories --------------------------------------------------

def get_private_dirs(form):
    return {
        'txt': path.join(_PRIVATE_DATA_FOLDER, form, 'veb', 'form'),
        'csv': path.join(_PRIVATE_DATA_FOLDER, form, 'veb', 'csv' )
    }

# Final assembly ------------------------------------------------------------
_DIRLIST = {
    '101'    : get_form_dirs('101'),
    '102'    : get_form_dirs('102'),
    'private101': get_private_dirs('101'),
    'private102': get_private_dirs('102'),
    'global' : {
        'database': path.join(_DIR_ROOT, 'database', 'db_dump'),
        'alloc'   : path.join(_DIR_ROOT, 'database', 'alloc'  ),
        'tables'  : path.join(_DIR_ROOT, 'database', 'tables' )
    }
}
# ---------------------------------------------------------------------------

def get_public_data_folder(form, subfolder_tag):
    """
    Return absolute path to public data folder.
    """
    return _DIRLIST[form][subfolder_tag]

def get_private_data_folder(form, subfolder_tag):
    """
    Return absolute path to private data folder.
    """
    return _DIRLIST['private' + form][subfolder_tag]

def get_global_folder(folder_tag):
    """
    Return absolute path to global folder with database files.
    """
    return _DIRLIST['global'][folder_tag]

def create_directories(dir_dict, verbose = False):
    """
    Create directories listed in <dir_dict> if such direcories fo not exist.
    To be used before downloading archived files from CBR server.
    """
    if verbose:
        print("Directories used:")
        
    for key, dir_ in dir_dict.items():
        if verbose:
            print(dir_)
            
        os.makedirs(dir_, exist_ok=True)

def create_default_directories():
    """
    Creates the default directories required by the application. Some
    directories can be configured by the user by editing the file "settings.cfg"
    in the project root.
    """
    for dirs in _DIRLIST.values():
        create_directories(dirs)

#############################################################################
# 2. DATABASE NAMES
#############################################################################

DB_NAME_RAW = 'dbf_db3'
DB_NAME_FINAL = 'cbr_db3'
DB_NAMES = {'raw': DB_NAME_RAW, 'final': DB_NAME_FINAL}

#############################################################################
#                3. FORM DESCRIPTIONS
#############################################################################

f101 = {
    'f101_B': {
        'tag': 'f101_B',
        'name': "bank accounts - short file",
        'postfix': "_B",
        'db_table': 'bulk_f101_b',
        'dbf_fields': ['DT', 'REGN', 'NUM_SC', 'A_P', 'ITOGO'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_B).DBF$"
    },

    'f101B1': {
        'tag': 'f101B1',
        'name': "bank accounts - long file",
        'postfix': "B1",
        'db_table': 'bulk_f101b1',
        'dbf_fields': ['DT', 'REGN', 'NUM_SC', 'A_P', 'IR', 'IV', 'IITG'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(B1).DBF$"
    }
}

f102 = {
    'f102_P': {
        'tag': 'f102_P',
        'name': "form 102 – short data",
        'postfix': "_P",
        'db_table': 'bulk_f102_P',
        'dbf_fields': ['DT', 'REGN', 'QUART', 'YEAR', 'CODE', 'ITOGO'],
        'regex': r"^([1-4])(20[0-9]{2})(_P).DBF$"
    },

    'f102P1': {
        'tag': 'f102_P1',
        'name': "form 102 – long data",
        'postfix': "_P1",
        'db_table': 'bulk_f102_P1',
        'dbf_fields': ['DT', 'REGN', 'QUART', 'YEAR', 'CODE', 'SIM_R', 'SIM_V', 'SIM_ITOGO'],
        'regex': r"^([1-4])(20[0-9]{2})(_P1).DBF$"
    }
}

FORM_DATA = {
    '101': f101,
    '102': f102
}

# Account names

ACCOUNT_NAMES_DBF = {
    '101': 'NAMES.DBF',
    '102': 'SPRAV1.DBF'
}

ACCOUNT_TABLE_NAME = {
    '101': "plan",
    '102': "sprav102"
}

ACCOUNT_TABLE_FIELDS = {
    '101': ("PLAN", "CONTO", "NAME", "LEVEL"),
    '102': ("NOM", "PRSTR", "CODE", "NAME")
}

ACCOUNT_DBF_FIELDS = {
    '101': ("PLAN", "NUM_SC", "NAME", "TYPE"),
    '102': ("NOM", "PRSTR", "CODE", "NAME")
}

def get_account_name_parameters(form):
    return ACCOUNT_TABLE_NAME[form], ACCOUNT_TABLE_FIELDS[form], ACCOUNT_DBF_FIELDS[form]

# Bank names

BANK_NAMES_DBF = (
    "[0-1][0-9]{5}_N.DBF",
    "[0-1][0-9]{5}N1.DBF"
)
BANK_TABLE_NAME = "bank"
BANK_TABLE_FIELDS = [("regn", "regn_name"), ("regn", "regn_name")]
BANK_DBF_FIELDS = [("REGN", "NAME_B"), ("REGN", "NAME_B")]

def get_bank_name_parameters():
    return BANK_TABLE_NAME, BANK_TABLE_FIELDS, BANK_DBF_FIELDS

#############################################################################
# 4. Additional paths
#############################################################################

MYSQL_PATH = [r'C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin', r'C:\MySQL\bin']

#############################################################################
# 5. General configuration
#############################################################################

# encoding of the dbf files
CODEPAGE = "cp866"

#############################################################################
# 6. DATABASE CONFIGURATION
#############################################################################

DB_INI_DICT = {'host': 'localhost', 'port':3306, 'user':'test_user', 'passwd':'test_password'}

