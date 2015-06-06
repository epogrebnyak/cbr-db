# Generic functions ::::::::::::::::::::::::::::::::::::::::::
def run_sql_file(file, dir):           
    sql_file = os.path.join(dir, file)    
    call_string = "mysql < {0}".format(sql_file)
    terminal(call_string)

def dump_table(db, table, dir):
    call_string = "mysqldump --fields-terminated-by=\\t\ --lines-terminated-by=\\r\\n --tab={0} {1} {2}".format(dir, db, table)
    terminal(call_string)
    replace_in_file(os.path.join(dir, table + ".txt") ,"\\","") 


    
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