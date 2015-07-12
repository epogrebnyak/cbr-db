# Tools to process Russian bank sector statistics 

**bankform.py** allows to import bank sector statistics stored as archived DBF files at [Bank of Russia website][cbr-forms] ("public data") to a local MySQL database, aggregate data into reports and save these reports in csv or xlsx format. The script can also import statistics stored locally in text form files ("private data"). 

[cbr-forms]: http://www.cbr.ru/credit/forms.asp

Principal steps taken in **bankform.py** are the following:

- Original archived DBF files are stored at [Bank of Russia website][cbr-forms]
- Download these ZIP/RAR files, unpack to get local DBF files
- Convert DBF files to CSV 
- Import CSV files to "raw data" database (large in size, contains all dates and banks)
- Truncate dataset and migrate it to "final use" database (smaller in size, just a few banks)
- Create output reports and write reports to CSV or XLSX files

For more information see:
- [Basic idea explained](https://github.com/epogrebnyak/cbr-db/wiki/Basic-idea-explained)
- [Dataflow charts](https://github.com/epogrebnyak/cbr-db/wiki/Dataflow-charts)  
- [Data structures](https://github.com/epogrebnyak/cbr-db/wiki/Data-structures)


## Interface

For full command line interface: 
```
python bankform.py 
```
or equivalent 
```
baf
```

## Sample script
The script below will download data and produce final balance sheet report for Jan 1, 2015 for reporting form 101. The final report files will be located in 'output' folder. 

```
python bankform.py reset database raw
python bankform.py reset database final    
python bankform.py download     101 2015-01-01
python bankform.py unpack       101 2015-01-01
python bankform.py make csv     101 2015-01-01
python bankform.py import csv   101 2015-01-01
python bankform.py make dataset 101 2015-01-01 
python bankform.py migrate dataset 101        
python bankform.py make   balance
python bankform.py report balance --xls
```

Same result shorter:

```
baf reset database 
baf update 101 2015-01
baf make dataset 101 2015-01  
baf migrate dataset 101        
baf make balance
baf report balance --xlsx
```

Check the output by ```dir ..\output``` or ```ls dir ..\output```. See [Testing milestones][tm] for more comments about these sample scipts.

[tm]: https://github.com/epogrebnyak/cbr-db/wiki/Testing-milestones


