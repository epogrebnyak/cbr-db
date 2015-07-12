bankform.py - list of vulnerabilities
--------------------------------------

general
--------

- do not like parts of the code style (naming, datastructures, similar things doen differently) - must inspect by file.

- not todo: on import table checksums not checked by design 

- some linux distributions have 'python' pointing to 'Python 2', while others
  have it pointing to 'Python 3'. Better default to using 'python3' on Linux, and
  'python' on Windows.  
  EP: Can be solved in baf.sh/baf.bat

- weak final use case of data, not provided 

- too slow: sql make_balance(), 

- no aggregation of form 102 yet

- tests for data integrity not invoked


milestones
----------

- simple scripts on Testig milestones run well (need reference output in new folder +  OK check with file compare)
- referfence dataset for database created locally
- same stored on a remote 

make_url.py
--------------
```
    bankform.py download   <form> (<timestamp1> [<timestamp2>] | --all-dates)
```

- get_url and get_ziprar_filename hardcoded (must be edited to support other forms)


make_csv.py
--------------
```
    bankform.py make csv   <form> (<timestamp1> [<timestamp2>] | --all-dates)
```

- write_csv_by_path hardcoded for form101 and f102

- 'make csv' may hang and not write all data from DBF to CSV, not checked
L: unable to reproduce

- inital DBF files not clean - may have 'lost' datasets (older data for a non-reporting bank in a newer file).
May import date of the file into database  

- import csv results in warnings on windows after commit 817c31a7bd82bfd96cd79b7717179ce7b6afb878,
  buth without those changes the import does not works on linux.
  
  database.py
-----------
Init:
```
    bankform.py reset   database [raw | final]
    bankform.py import plan <form>
    bankform.py import bank
```

Raw database:   
``` 
    bankform.py make dataset <form> <timestamp1> [<timestamp2>] [--regn=<regn_list> | --regn-file=<file> | --regn-all]
    bankform.py save    dataset <form>
    bankform.py import  dataset <form>
    bankform.py migrate dataset <form>
```

Final database:
```
    bankform.py import alloc
    bankform.py import tables
    bankform.py make   balance
    bankform.py test  balance
    bankform.py report balance     [--xlsx]
    bankform.py report form <form> [--xlsx]
```

- hardcoded insert on `import_bank`:
  execute_sql(u"INSERT IGNORE INTO bank (regn, regn_name) VALUE (964, 'Внешэкономбанк')", db)

- import_bank is hardcoded for form101 (as form 102 will reuse the data from 101)

- 'insert ignore' may be hiding bugs in the code (ex.: issue #25)

- dependecy on mysql* executables

- make dataset seems to be too slow for what it is doing - missing indexes?
  
- when reseting the `final` database, the following errors are issued:
ERROR 1406 (22001) at line 11 in file: 'tables\plan.sql': Data too long for column 'plan' at row 1
and
mysqlimport: Error: 1366, Incorrect integer value: '\xD0\x9A\xD0\xBE\xD0\xB4\x0D' for column 'line' at row 1, when using table: balance_line_name

- depends on GROUP_CONCAT for dumping CSV files with columns  
L: Is this still used? Found not references for GROUP_CONCAT outside the abandoned folder.
EP: it is part of stored SQL procedures

- bankform.py import alloc and bankform.py import tables are a weakness

- saparate into general database access functions and script-specific functions? 

private_form_txt.py
---------------------
```
    bankform.py make csv   <form> --private-data [--all-dates]
    bankform.py import csv <form> --private-data [--all-dates]
```

- form102 private data importer skips rows with missing or invalid values

- The private textual data can't be found anymore as the old directory structure separated them by years.
  This is a known issue and must be fixed before --private-data flag works again.
  Related to the now missing yearly subdirectories.

- private data not handled in a uniform way with rest of data
 
global_ini.py
-------------

- enable yearly subdirectories in both public and private data directories

cli_dates.py
------------

- minor issue: 'allows future dates in form 102 and crashes on a future date in 101.'


pandas interface
----------------
- code not optimised
