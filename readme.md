# bankform.py: import and process Russian banking sector statistics 

**bankform.py** allows to import bank sector statistics stored as archived DBF files at [Bank of Russia website][cbr-forms] ("public data") to a local MySQL database, aggregate data into reports and save these reports in csv or xlsx format. The script can also import statistics stored locally in text form files ("private data"). 

Archived DBF files at Bank of Russia web site contain detailed monthly and quarterly bank reporting forms as well as reporting form descriptions and bank names. These files can be found here: [http://www.cbr.ru/credit/forms.asp][cbr-forms] 

[cbr-forms]: http://www.cbr.ru/credit/forms.asp

## Data flow and interface

Data is processed arroding to the following chain:

Bank of Russia web site -> Local ZIP/RAR files -> Local DBF files -> Local CSV files -> Large raw database -> Smaller final database -> Reports in CSV of XLSX files

## Interface

For full commandline interface: 
''
python bankform.py 
''
## Sample script
The script below will download data and produce final balance sheet report for Jan 1, 2015 for reporting form 101. The final report files will be located in 'output' folder.

''
  python bankform.py reset database raw
	python bankform.py reset database final    
  python bankform.py download   101 2015-01-01
	python bankform.py unpack     101 2015-01-01
	python bankform.py make csv   101 2015-01-01
	python bankform.py import csv 101 2015-01-01
    python bankform.py migrate dataset 101        
    python bankform.py make   balance
    python bankform.py report balance --xls
	dir ..\output
''

Same result shorter:
''
    python bankform.py reset database 
    python bankform.py update 101 2015-01-01
	python bankform.py migrate dataset 101        
    python bankform.py make   balance
    python bankform.py report balance --xls
	dir ..\output
''
