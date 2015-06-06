"""Usage: 
   bankform.py pass
   bankform.py newdb <db>

   bankform.py download --form 101 --date <date> 
   bankform.py download --form 101 --date-start <date_start> [--date-end <date_end>]
   bankform.py download --form 101 --year-start <year_start> [--year-end <year_end>]
   bankform.py unpack   --form 101 [--date <date>] [-all]
   
   bankform.py make csv --form 101 --all
   bankform.py make csv --form 101 --date <date> 
   bankform.py make csv --form 101 --date-start <date_start> [--date-end <date_end>]
   bankform.py make csv --form 101 --year-start <year_start> [--year-end <year_end>]
   
   bankform.py import csv --form 101 --date <date> 
   bankform.py import csv --form 101 --date-start <date_start> [--date-end <date_end>]
   bankform.py import csv --form 101 --year-start <year_start> [--year-end <year_end>]

   bankform.py make balance [--add-test]
   bankform.py test balance 
   bankform.py report balance [--dir <directory>]
   
   bankform.py import alloc --file <filename> [--dir <directory>]
"""

# Не сделано:
# python bankform.py download   --form 101 --year-start 2012 --year-end 2014
# python bankform.py unzip      --form 101 --year-start 2012 --year-end 2014
# python bankform.py make csv   --form 101 --year-start 2012 --year-end 2014
# python bankform.py import csv --form 101 --date 1.1.2015
# python bankform.py migrate    --form 101 --regn-list regn.txt

# todo:
# py: import tables from one directory (import table <filename>) dos: change to roll.bat and dir structure
# all with dates


import sys
import os
import time
from terminal import terminal
from make_url import get_101_filelist
from make_csv import mass_convert_to_csv, write_csv_by_date, make_csv_filenames
import date_engine



EOL = "\n"

# this file is in subfolder of DIR_ROOT 
DIR_ROOT         = os.path.dirname(
                   os.path.dirname(os.path.abspath(__file__))
                                  )

WGET_PATH        = "C:\\Program Files (x86)\\GnuWin32\\bin\\wget.exe"
UNRAR_PATH       = os.path.join(DIR_ROOT, 'bin/unrar')
Z7_PATH          = os.path.join(DIR_ROOT, 'bin/7za')

DIR_IMPORT_ALLOC = os.path.join(DIR_ROOT, 'data.db/alloc')
DIR_BALANCE      = os.path.join(DIR_ROOT, 'task/balance')
DIR_REPORT       = os.path.join(DIR_ROOT, 'output')
DIR_DATA         = os.path.join(DIR_ROOT, 'data.downloadable')

DIR_CSV_101      = os.path.join(DIR_DATA, '101/csv.full')
DIR_DBF_101      = os.path.join(DIR_DATA, '101/dbf')
DIR_RAR_101      = os.path.join(DIR_DATA, '101/rarzip')

'''
set              "DBF_DIR=%data_dir%\101\dbf"
set       "CSV_DIR_UPDATE=%data_dir%\101\csv.update"
set "CSV_DIR_FULL_ARCHIVE=%data_dir%\101\csv.full"
set              "SQL_DIR=%data_dir%\101\sql"
set              "RAR_DIR=%data_dir%\101\rarzip"

:: Private data 
set "DATA_DIR_PRIVATE=%BASE_DIR%\data.private"
set     "FORM_DIR_VEB=%data_dir_private%\veb\form"
set      "CSV_DIR_VEB=%data_dir_private%\veb\csv"
'''

# Generic functions ::::::::::::::::::::::::::::::::::::::::::
def run_sql_file(file, dir):           
    sql_file = os.path.join(dir, file)    
    call_string = "mysql < {0}".format(sql_file)
    terminal(call_string)

def dump_table(db, table, dir):
    call_string = "mysqldump --fields-terminated-by=\\t\ --lines-terminated-by=\\r\\n --tab={0} {1} {2}".format(dir, db, table)
    terminal(call_string)
    replace_in_file(os.path.join(dir, table + ".txt") ,"\\","") 

def replace_in_file(filepath,replace_what,replace_with):
    with open(filepath) as f:
         lines = f.read().replace(replace_what,replace_with)
    with open(filepath, 'w') as f1: 
         f1.write(lines)
         
def in_quotes(str):
    return '"' + str + '"'


# Command-line commands ::::::::::::::::::::::::::::::::::::::::::
def import_generic(filename, directory, mysqlimport_string):
    path = os.path.join(directory, filename)
    if os.path.isfile(path):
        call_string = mysqlimport_string.format(path)    
        terminal(call_string)
    else: 
        print("File not found:",  path)

def import_alloc(filename):
    import_generic(filename, DIR_IMPORT_ALLOC, 
                   "mysqlimport cbr_db2 {0} --delete")

def import_csv(filename):
    import_generic(filename, DIR_CSV_101, 
                   "mysqlimport dbf_db {0} --ignore_lines=1 --ignore ")
    
def make_balance(run_test = False):
    run_sql_file('balance-make.sql', DIR_BALANCE)
    if run_test == True:
        test_balance()

def test_balance():
    run_sql_file('balance-test.sql', DIR_BALANCE) 

def report_balance(table_names):
   run_sql_file('balance-report.sql', DIR_BALANCE) 
   for table in table_names:
       dump_table('cbr_db2', table, DIR_REPORT)       
   # todo - delete all sql in DIR_REPORT 
   # if exist %DIR_OUTPUT%\%1.sql (del %DIR_OUTPUT%\%1.sql)
 
def unpack(filepath, destination_directory):
    ext = os.path.splitext(filepath)[1].lower()  
    print(ext)    
    if ext == '.rar':    
        call_string = " ".join([in_quotes(UNRAR_PATH)
                               , "e" , filepath             
                               , destination_directory
                               , "-y"])
    else:
        # call    bin\7za e data.db\201412f101.7z -odata.downloadable\101\dbf -y  
        call_string = " ".join([in_quotes(Z7_PATH) 
                               , "e" , filepath             
                               , "-o" + destination_directory
                               , "-y"])    
        terminal (call_string)  

                               
def download_f101(start_date, end_date, exe = WGET_PATH, dir = DIR_RAR_101, method = 'wget_no_file'):
    """Make a list of URLs in txt file and downloads these URLs to local folder using wget
    """ 
    if method == 'wget_no_file':
        for url in get_101_filelist(start_date, end_date):
        # wget -N -P D:\temp\101\rarzip\ <file>
            call_string = " ".join([in_quotes(exe) ,  "-N", 
                                    "-P", in_quotes(dir), 
                                    in_quotes(url)])
            terminal (call_string)  
 
def extend_date_arguements(arg):
    s = None
    e = None    
    if arg['--date-start'] is True: 
        # check format for date YYYY-MM-DD or YYYY-DD
        # check if date makes sense
        s = arg['<date_start>']
        # if not supplied make it today
        e = arg['<date_end>']    
    elif arg['--year-start'] is True:
        # make s start of year  1-Jan      
        s = arg['<year_start>']
        # make end of year 1-Jan year + 1 or current month start
        e = arg['<year_end>']    
    elif arg['--date'] is True:
        # check format for date YYYY-MM-DD or YYYY-DD
        # check if date makes sense
        s = arg['<date>']
        e = s
    return date_engine.get_isodate_list(s, e) 
    
# Docopt ::::::::::::::::::::::::::::::::::::::::::
from docopt import docopt

if __name__ == '__main__':
    arg = docopt(__doc__)    
# print('Argument string:', arg)
  
# download
if arg['download'] is True and arg['--form'] == "101": 
    s, e = get_date_range(arg) 
    print (s, e)
    download_f101(s, e)

# unpack
if arg['unpack'] is True and arg['--form'] == "101": 
    for file in os.listdir(DIR_RAR_101):
        unpack(os.path.join(DIR_RAR_101,file), DIR_DBF_101)   
        
# import alloc  
if arg['import'] is True and arg['alloc'] is True: 
   filename = arg["<filename>"]
   import_alloc(filename)
        
# make csv
if arg['make'] is True and arg['csv'] is True: 
   #if arg['<date>'] is not None:
   #   isodate = arg['<date>']
   #   print ("Selected date:", isodate)
   #   write_csv_by_date(isodate, dbf_dir = DIR_DBF_101, csv_dir = DIR_CSV_101)
   
   for isodate in extend_date_arguements(arg):
      print ("Selected date:", isodate)
      write_csv_by_date(isodate, dbf_dir = DIR_DBF_101, csv_dir = DIR_CSV_101)
         
   # note: this is legacy call based on full directory listing, needs review
   if arg['--all'] is True:
       used_file_types = ("f101_B", "f101B1")
       for file_type in used_file_types: 
            mass_convert_to_csv(file_type, dbf_directory = DIR_DBF_101, csv_directory = DIR_CSV_101)

# import csv  
if arg['import'] is True and arg['csv'] is True: 
   for isodate in extend_date_arguements(arg):
      print ("Selected date:", isodate)
      for csv_fn in make_csv_filenames(isodate, '101'):
          print (csv_fn)
          import_csv(csv_fn)   
   
# make balance
if arg['make'] is True and arg['balance'] is True: 
   run_test = arg["--add-test"]
   make_balance(run_test)
   
# test balance
if arg['test'] is True and arg['balance'] is True: 
   test_balance()
   
# report balance
if arg['report'] is True and arg['balance'] is True:    
   table_names = ("tmp_output_itogo", "tmp_output_ir", "tmp_output_iv")
   report_balance(table_names)  
