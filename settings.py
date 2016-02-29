"""
Settings file for cbr_db.

You can specify a different settings file
using CBR_DB_SETTINGS environment variable.
"""

# QUESTION: Where is CBR_DB_SETTINGS defined, how one can modify it?

import os
import platform

IS_WINDOWS = (platform.system() == 'Windows')

#
# MySQL
#

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'test_user'
MYSQL_PASSWORD = 'test_password'
MYSQL_PATHS = []
if IS_WINDOWS:
    MYSQL_PATHS.extend([
        'C:\\Program Files (x86)\\MySQL\\MySQL Server 5.7\\bin',
        'C:\\MySQL\\bin', 
        'D:\\Programs\\xampp\\mysql\\bin'
    ])

#
# Database names
#
    
DB_NAME_RAW = 'dbf_db'
DB_NAME_FINAL = 'cbr_db'

#
# Paths and directories
#

_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_PROJECT_DIR, 'data')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

if IS_WINDOWS:
    UNPACK_RAR_EXE = os.path.join(_PROJECT_DIR, 'bin', 'unrar.exe')
else:
    UNPACK_RAR_EXE = 'unrar'