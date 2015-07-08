Deployment notes (draft)
================

bankform.py requires following system and script configuration.

MySQL
-----

1. MySQL server daemon must be up and running when bankform.py is started. 

2. mysql, mysqlimport, mysqldmp (collectively - "mysql*.exe") must be callable from command line. For that:
2.1. config file 'my.ini' or 'my.cfg' must contain valid host, user, password to allow mysql*.exe calls from command line 
2.2. mysql*.exe must be in PATH. If not in PATH run utils\ini.bat with correct path to mysql directory.

3. (NOT IMPLEMENTED) 

Paths to 7z and unrar
---------------------


Database credentials
--------------------
duplication?
