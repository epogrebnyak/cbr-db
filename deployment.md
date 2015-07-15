Deployment notes (draft)
================

bankform.py requires following system and script configuration.

MySQL
-----

1. MySQL server daemon must be up and running when bankform.py is started. 

2. [mysql] section in <settings.cfg> must contain valid username, password, port and host to access MySQL database.

3. mysql, mysqlimport, mysqldump (collectively - "mysql\*.exe") must be callable from command line.  
For that:  
a) config file 'my.ini' or 'my.cfg' must contain valid host, user, password to allow mysql\*.exe calls from command line   
b) mysql\*.exe must be in PATH on Windows. If not in PATH run utils\ini.bat with correct path to mysql directory.

* Development note: conn.py and database.py use MySQL

Paths to 7z and unrar
---------------------
bankform.py uses ```7z``` and ```unrar``` executables to unpack .zip and .rar files. Binaries for Windows systems are in \bin\ subfolder of project directory. On Linux must install these binaries with: 
```
apt-get install 7z
apt-get install unrar
```
bankform.py attempts to run 7z and unrar from command line on Linux and using path on Windows. Path is configurable in [zip/rar path] in settings.cfg, but not recommended to alter.

* Development note: handling of paths is in config_folders.py

Directory structure - where data is?
------------------------------------
By default bankform.py will create a data directory in project folder and store downloaded and processed information there. Settings.cfg can alter these paths (see comments in  settings.cfg) 
Intent to alter the paths can be for example - storing data in a separate folder, accessible by other programs/users. 

* Development note: handling of directories is in config_folders.py

Test deployment
---------------
* Development note: may add 'baf selftest' for trial calls of functions with dependcies. Also some Windows diagnostics in old roll.bat file.
