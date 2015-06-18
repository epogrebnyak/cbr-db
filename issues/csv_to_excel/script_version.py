from xlwings import Range, Workbook, Chart, Sheet
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import datetime
from datetime import datetime
import os
import sys

## variable define
## Output directory of XlS
xls_dir = "c:\\Users\\R5311656\\Desktop\\Script\\xls\\"

## CSV file paths 
file_itogo = "c:\\Users\\R5311656\\Desktop\\Script\\csv\\tmp_output_itogo.txt"
file_ir = "c:\\Users\\R5311656\\Desktop\\Script\\csv\\tmp_output_ir.txt"
file_iv = "c:\\Users\\R5311656\\Desktop\\Script\\csv\\tmp_output_iv.txt"



## file name prepare
today = datetime.now()
datetime = today.strftime("%Y_%m_%d_%H-%M")


## CVS File check exist or not & Size 


if os.path.isfile(file_itogo or file_ir or file_iv):
   
	if os.stat(file_itogo or file_ir or file_iv).st_size > 0:
		## Open new Workbook


		wb = Workbook(app_visible=False )
		# Prepare first sheet

		sheet1 = pd.read_csv(file_itogo, delim_whitespace=True)

		Sheet.add('csv_itogo',before='Sheet1')

		Range('csv_itogo','A1',index=False).value =sheet1

		Range('csv_itogo','A:ZZ').autofit('c')

		# Prepare Second sheet

		sheet2 = pd.read_csv( file_ir, delim_whitespace=True)

		Sheet.add('csv_ir',after='csv_itogo')

		Range('csv_ir','A1',index=False).value = sheet2

		Range('csv_ir','A:ZZ').autofit('c')



		# Prepare Third Sheet
		sheet3 = pd.read_csv(file_iv, delim_whitespace=True)

		Sheet.add('csv_iv',after='csv_ir')

		Range('csv_iv','A1',index=False).value = sheet3

		Range('csv_iv','A:ZZ').autofit('c')



		# Save WorkSheet
		xlspath = xls_dir + "reference_view_balance_" + datetime + ".xlsx"
		wb.save(xlspath)
		wb.close()

		# Empty Files

		open( file_itogo,"w").close()
		open( file_ir,"w").close()
		open( file_iv,"w").close()
	else:
			print ( "Check File Size, It shouldn't be empty")
else:
		print ("Check All files exists ")
	
	
