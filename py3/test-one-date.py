import ini
import os

def pyrun(cmd):
    os.system("python {}".format(cmd))

if __name__ == '__main__':
    ini.check_mysql_path()
    pyrun("bankform.py reset database raw")
    pyrun("bankform.py reset database final")
    pyrun("bankform.py download 101 --date 2015-01-01")
    pyrun("bankform.py unpack   101 --date 2015-01-01")
    pyrun("bankform.py make csv 101 --date 2015-01-01")
    pyrun("bankform.py import csv  101 --date 2015-01-01")
    pyrun("bankform.py make dataset 101")
    pyrun("bankform.py migrate dataset 101")
    pyrun("bankform.py import alloc")
    pyrun("bankform.py import tables")
    pyrun("bankform.py make balance")
    pyrun("bankform.py report balance")
    pyrun("bankform.py test balance")
