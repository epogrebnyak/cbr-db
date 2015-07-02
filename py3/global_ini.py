import os

# variables imported to other modules from here: 
# PATH, DIRLIST, DB_NAMES, FORM_DATA, MYSQL_PATH

# this global_ini.py file is in subfolder of DIR_ROOT, do os.path.dirname() twice
DIR_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#############################################################################
# 0. EXECUTABLES
#############################################################################
 
# Executables directories
PATH = {'unrar': os.path.join(DIR_ROOT, 'bin', 'unrar.exe'), 
           'z7': os.path.join(DIR_ROOT, 'bin', '7za')}

#############################################################################
# 1. DATA DIRECTORIES
#############################################################################

# todo: directory structure of DIRLIST is a bit of a mess, correct it
#       see composition of DIRLIST
#       maybe add fuctions such as:

# Form directories
DIR_DATA = os.path.join(DIR_ROOT, 'data.downloadable')

def get_form_dirs(form):
    return {
        'rar': os.path.join(DIR_DATA, form, 'rarzip'  ),
        'dbf': os.path.join(DIR_DATA, form, 'dbf'     ),
        'csv': os.path.join(DIR_DATA, form, 'csv.full'),
        'output': os.path.join(DIR_ROOT, 'output')
        # 'sql': DIR_SQL_101,
    }

# todo: 'output' may be a global directory in GLOB_DIR, not a form 101  directory
#        find where it is used and change

# commented: SQL directory not used, writing sql dumps to output instead
#         DIR_SQL_101 = os.path.join(DIR_DATA, '101', 'sql')

# Making of GLOB_DIR --------------------------------------------------------
GLOB_DIR = {
    'database': os.path.join(DIR_ROOT, 'database', 'db_dump'),
    'alloc'   : os.path.join(DIR_ROOT, 'database', 'alloc'  ),
    'tables'  : os.path.join(DIR_ROOT, 'database', 'tables' )
}

# Private data directories --------------------------------------------------
EXTRA_DIR = {'101': 
                    {'txt': os.path.join(DIR_ROOT, 'data.private', 'veb', 'form'),
                     'csv': os.path.join(DIR_ROOT, 'data.private', 'veb', 'csv' )
                     }
            }
            
# Final assembly ------------------------------------------------------------
DIRLIST = {
    '101'    : get_form_dirs('101'),
    '102'    : get_form_dirs('102'),
    'global' : GLOB_DIR,
    'private': EXTRA_DIR
}
# ---------------------------------------------------------------------------

# Tentative structure:
# global + database, alloc, tables, output
# 101 + public  + rar, dbf, csv
# 101 + private + txt, csv

def get_public_data_folder(form, subfolder_tag):
    """
    Return absolute path to public data folder.
    """
    return DIRLIST[form][subfolder_tag]

def get_private_data_folder(form, subfolder_tag):
    """
    Return absolute path to private data folder.
    """
    return EXTRA_DIR[form][subfolder_tag]
    
def get_global_folder(folder_tag):
    """
    Return absolute path to global folder with database files.
    """
    return GLOB_DIR[folder_tag]    

def create_directories(dir_dict, verbose = False):
    """
    Create directories listed in <dir_dict> if such direcories fo not exist.
    To be used before downloading archived files from CBR server.
    """
    if verbose: print("Directories used:")
    for key, dir_ in dir_dict.items():
        if verbose: print(dir_)
        os.makedirs(dir_, exist_ok=True)

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

ACCOUNT_NAMES_DBF = {
    '101': 'NAMES.DBF',
    '102': 'SPRAV1.DBF'
}

ACCOUNT_TABLE_NAME = {
    '101': "sprav101",
    '102': "sprav102"
}

ACCOUNT_TABLE_FIELDS = {
    '101': ("PLAN", "NUM_SC", "NAME", "TYPE"),
    '102': ("NOM", "PRSTR", "CODE", "NAME")
}

BANK_TABLE_NAME = {
    '101': "bank101",
    '102': "bank102"
}

BANK_TABLE_FIELDS = {
    '101': ("REGN", "NAME_B", "PRITZ", "PRITZ_P")
}

def get_account_name_parameters(form):
    return ACCOUNT_TABLE_NAME[form], ACCOUNT_TABLE_FIELDS[form]

def get_bank_name_parameters(form):
    return BANK_TABLE_NAME[form], BANK_TABLE_FIELDS[form]

############################################################################# 
# 4. Additional paths
#############################################################################

MYSQL_PATH = [r'C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin', r'C:\MySQL\bin']

############################################################################# 
# 5. General configuration
#############################################################################

# encoding of the dbf files
CODEPAGE = "cp866"
