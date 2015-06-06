# EP: main comment - the directory structure is given in global_ini.DIRLIST dictionary
#     so this file should rather iterate over form and directories in global_ini.DIRLIST
#     and call os.makedirs to create it.

import os
from os.path import join

# EP: why print this? it is a comment in file. make it more visible?
print('10:07 28.05.2015')
print('Note: may merge CSV_DIR_UPDATE and CSV_DIR_FULL_ARCHIVE')

# simulates the bat ~dp0, geting the directory of the script 
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DATA_DIR             = join(BASE_DIR, 'data.downloadable')
DBF_DIR              = join(DATA_DIR, '101', 'dbf')
CSV_DIR_UPDATE       = join(DATA_DIR, '101', 'csv.update')
CSV_DIR_FULL_ARCHIVE = join(DATA_DIR, '101', 'csv.full')
SQL_DIR              = join(DATA_DIR, '101', 'sql')
RAR_DIR              = join(DATA_DIR, '101', 'rarzip')

# Private data
DATA_DIR_PRIVATE = join(BASE_DIR, 'data.private')
FORM_DIR_VEB = join(DATA_DIR_PRIVATE, 'veb', 'form')
CSV_DIR_VEB = join(DATA_DIR_PRIVATE, 'veb', 'csv')

# Output
DIR_OUTPUT = join(BASE_DIR, 'output')

# Create directories
DIRS = [DATA_DIR, DBF_DIR, CSV_DIR_UPDATE, CSV_DIR_FULL_ARCHIVE, RAR_DIR, SQL_DIR, DIR_OUTPUT]

for dir_ in DIRS:
    os.makedirs(dir_, exist_ok=True)

print('Directories checked or created')
