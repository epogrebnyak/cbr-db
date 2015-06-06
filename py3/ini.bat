:: MySQL
PATH %PATH%;"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin"

echo Paths to MysqL updated...


mysql -e "quit();" 2> NUL
if %errorlevel%==9009 (
   echo Path to MySQL directory is not correct. Update paths in this bat file.
   goto end
  ) else (echo Mysql path ok )

