exec ini.bat
cd ..
python bankform.py reset database raw
python bankform.py reset database final
python bankform.py download  102 2015Q1
python bankform.py unpack  102 2015Q1
python bankform.py make csv  102 2015Q1
python bankform.py import csv 102 2015Q1
python bankform.py make dataset 102
python bankform.py migrate dataset 102
python bankform.py import alloc
python bankform.py import tables
python bankform.py make balance
python bankform.py test balance
python bankform.py report balance