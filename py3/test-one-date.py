import ini
import os

def get_exec():
    print('** detecting python3 executable **')

    if os.system('python3 --version') == 0:
        return 'python3'
    else:
        return 'python'

def pyrun(exec_, cmd):
    if os.system("{} {}".format(exec_, cmd)) != 0:
        raise RuntimeError('The command "{}" has failed. Aborting.'.format(cmd))

if __name__ == '__main__':
    ini.check_mysql_path()
    exec_ = get_exec()

    pyrun(exec_, "bankform.py reset database raw")
    pyrun(exec_, "bankform.py reset database final")
    pyrun(exec_, "bankform.py download 101 2015-01-01")
    pyrun(exec_, "bankform.py unpack   101 2015-01-01")
    pyrun(exec_, "bankform.py make csv 101 2015-01-01")
    pyrun(exec_, "bankform.py import csv  101 2015-01-01")
    pyrun(exec_, "bankform.py make dataset 101")
    pyrun(exec_, "bankform.py migrate dataset 101")
    pyrun(exec_, "bankform.py import alloc")
    pyrun(exec_, "bankform.py import tables")
    pyrun(exec_, "bankform.py make balance")
    pyrun(exec_, "bankform.py test balance")
    pyrun(exec_, "bankform.py report balance")
    
    #os.system("""mysql dbf_db3 --execute="SET max_error_count=3000; LOAD DATA INFILE  'C:/Users/Lucas/Desktop/ep_bf/data.downloadable/101/csv.full/bulk_f101_b.122014_B' IGNORE INTO TABLE bulk_f101_b IGNORE 1 LINES; SHOW WARNINGS" > warningsA.txt""")
    #os.system("""mysql dbf_db3 --execute="SET max_error_count=3000; LOAD DATA INFILE  'C:/Users/Lucas/Desktop/ep_bf/data.downloadable/101/csv.full/bulk_f101b1.122014B1' IGNORE INTO TABLE bulk_f101b1 IGNORE 1 LINES; SHOW WARNINGS" > warningsB.txt""")
    