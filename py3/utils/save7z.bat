REM Save folder to ep_bf.7z
REM 10:12 18.06.2015

if []==[%1] (set "filename=ep_bf.7z" 
  ) else (set "filename=%1")

REM Move to root folder
cd..
cd..

del %filename%
bin\7za a %filename% * -xr!data.downloadable -xr!output -xr!data.private -x!%filename% -xr!py3\__pycache__\
