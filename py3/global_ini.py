import os

# 1. DIRECTORIES
# this file is in subfolder of DIR_ROOT
DIR_ROOT = os.path.dirname(
           os.path.dirname(os.path.abspath(__file__))
           )

# Executables directories          
UNRAR_PATH = os.path.join(DIR_ROOT, 'bin', 'unrar.exe')
Z7_PATH    = os.path.join(DIR_ROOT, 'bin', '7za')
MYSQL_PATH = r'C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin'
PATH = {'unrar': UNRAR_PATH, 'z7': Z7_PATH}

# Public data directories          
DIR_DATA    = os.path.join(DIR_ROOT, 'data.downloadable')
DIR_OUTPUT  = os.path.join(DIR_ROOT, 'output')
DIR_CSV_101 = os.path.join(DIR_DATA, '101', 'csv.full')
DIR_DBF_101 = os.path.join(DIR_DATA, '101', 'dbf')
DIR_RAR_101 = os.path.join(DIR_DATA, '101', 'rarzip')
DIR_SQL_101 = os.path.join(DIR_DATA, '101', 'sql')
DIR101  = {'rar': DIR_RAR_101, 'dbf': DIR_DBF_101, 'csv': DIR_CSV_101, 'sql': DIR_SQL_101,
           'output': DIR_OUTPUT}
# 'output' may be a global directory  
           
DIR_GLOBAL_SQL = os.path.join(DIR_ROOT,       'database')          
DIR_ALLOC      = os.path.join(DIR_GLOBAL_SQL, 'alloc')          
DIR_TABLES     = os.path.join(DIR_GLOBAL_SQL, 'tables')          
           
GLOB_DIR = {'database':DIR_GLOBAL_SQL,
               'alloc':DIR_ALLOC,
              'tables':DIR_TABLES} 
               

DIRLIST = {   '101': DIR101,
           'global': GLOB_DIR}


# Private data directories          
EXTRA_DIR_101_TXT = os.path.join(DIR_ROOT, 'data.private', 'veb', 'form')
EXTRA_DIR_101_CSV = os.path.join(DIR_ROOT, 'data.private', 'veb', 'csv')
EXTRA_DIR = {'101': {'txt': EXTRA_DIR_101_TXT, 'csv': EXTRA_DIR_101_CSV}}

def create_directories(dir_dict):
    print ("Directories used:")
    for key, dir_ in dir_dict.items():        
        print(dir_)    
        os.makedirs(dir_, exist_ok=True)

# 2. DATABASE NAMES
DB_NAME_RAW   = 'dbf_db3'
DB_NAME_FINAL = 'cbr_db3'       
DB_DICT = {'raw': DB_NAME_RAW, "final": DB_NAME_FINAL}
    

# 3. FORM DESCRIPTIONS

f101 = {
    'f101_B': {'tag': 'f101_B',
    'name': "bank accounts - short file",
    'postfix': "_B",
    'db_table': 'bulk_f101_b',
    'dbf_fields': ['DT', 'REGN', 'NUM_SC', 'A_P', 'ITOGO'],
    'regex': r"^([0-9]{2})(20[0-9]{2})(_B).DBF$"  },

    'f101B1': {'tag': 'f101B1',
    'name': "bank accounts - long file",
    'postfix': "B1",
    'db_table': 'bulk_f101b1',
    'dbf_fields': ['DT', 'REGN', 'NUM_SC', 'A_P', 'IR', 'IV', 'IITG'],
    'regex': r"^([0-9]{2})(20[0-9]{2})(B1).DBF$"  }
}

FORM_DATA = {'101': f101}