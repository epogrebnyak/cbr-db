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
    pyrun(exec_, "bankform.py download 101 --date 2015-01-01")
    pyrun(exec_, "bankform.py unpack   101 --date 2015-01-01")
    pyrun(exec_, "bankform.py make csv 101 --date 2015-01-01")
    pyrun(exec_, "bankform.py import csv  101 --date 2015-01-01")
    pyrun(exec_, "bankform.py make dataset 101")
    pyrun(exec_, "bankform.py migrate dataset 101")
    pyrun(exec_, "bankform.py import alloc")
    pyrun(exec_, "bankform.py import tables")
    pyrun(exec_, "bankform.py make balance")
    pyrun(exec_, "bankform.py report balance")
    pyrun(exec_, "bankform.py test balance")
