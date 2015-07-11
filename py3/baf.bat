@echo off
REM Short-call wrapper for python bankform.py
REM Allows to call 'baf reset database' instead of 'python bankform.py reset database' 
REM This saves a bit of time typing.
python bankform.py %1 %2 %3 %4 %5 %6 %7 %8
