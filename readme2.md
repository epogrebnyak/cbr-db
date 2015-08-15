

Principal fields by form: 
- form 101:  
regn - dt - conto - ir - iv - itogo

- form 102:  
...

Main job: 
   - create SQLite in-memory table for storing data from form 101 and 102
   - generate data stream from DBF files based on names of columns
   - dump data stream to csv
   - write data stream to database to obtain full database
   - truncate dataset by 'regn' and 'date' and write it to obtain smaller final database

Optionally:
   - filter data stream to omit unnecessary rows (write omitted rows to different stream)
   - test data consistency 
 

