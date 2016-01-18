"""
Settings file for cbr_db.

You can specify a different settings file
using CBR_DB_SETTINGS environment variable.
"""

import os
import platform

_PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
_WINDOWS = (platform.system() == 'Windows')

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'test_user'
MYSQL_PASSWORD = 'test_password'
MYSQL_PATH = []
if _WINDOWS:
    MYSQL_PATH.extend([
        'C:\\Program Files (x86)\\MySQL\\MySQL Server 5.7\\bin',
        'C:\\MySQL\\bin'
    ])

_DATA_FOLDER = os.path.join(_PROJECT_FOLDER, 'data')
PUBLIC_DATA_FOLDER = os.path.join(_DATA_FOLDER, 'downloadable')
PRIVATE_DATA_FOLDER = os.path.join(_DATA_FOLDER, 'private')
OUTPUT_FOLDER = os.path.join(_DATA_FOLDER, 'output')


if _WINDOWS:
    UNPACK_7Z_EXE = os.path.join(_PROJECT_FOLDER, 'bin', '7za.exe')
    UNPACK_RAR_EXE = os.path.join(_PROJECT_FOLDER, 'bin', 'unrar.exe')
else:
    UNPACK_7Z_EXE = '7z'
    UNPACK_RAR_EXE = 'unrar'
