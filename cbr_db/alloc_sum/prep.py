import pandas as pd
import numpy as np

REGN = 1010
    
def flatten(source_df, key_col):    
    col_dict  = {	
    '2010-01-01' : [2009,	'2009_ir',	'2009_iv'],
	'2011-01-01' : [2010,	'2010_ir',	'2010_iv'],
	'2012-01-01' : [2011,	'2011_ir',	'2011_iv'],
	'2013-01-01' : [2012,	'2012_ir',	'2012_iv'],
	'2014-01-01' : [2013,	'2013_ir',	'2013_iv'],
	'2015-01-01' : [2014,	'2014_ir',	'2014_iv'],
	'2015-04-01' : ['20150401',	'20150401_ir',	'20150401_iv'],
	'2015-05-01' : ['20150501',	'20150501_ir',	'20150501_iv'],
	'2015-07-01' : ['20150701',	'20150701_ir',	'20150701_iv'],
	'2015-08-01' : ['20150801',	'20150801_ir',	'20150801_iv'],
	'2015-09-01' : ['20150901',	'20150901_ir',	'20150901_iv'],
	'2015-10-01' : ['20151001',	'20151001_ir',	'20151001_iv'],
	'2015-11-01' : ['20151101',	'20151101_ir',	'20151101_iv'],
	'2015-12-01' : ['20151201',	'20151201_ir',	'20151201_iv'],
	'2016-01-01' : ['20160101',	'20160101_ir',	'20160101_iv'] }
    
    df = pd.DataFrame()
    for dt, cols in col_dict.items(): # '2016-01-01':             
        df_block = source_df[[key_col] + cols]
        df_block ['dt'] = dt
        df_block = df_block.rename(index=str, columns={cols[0]:'itogo', cols[1]:'ir', cols[2]:'iv'})
        df = df.append(df_block)
    df['regn'] = REGN 
    return df
    
    
xl_filename = 'summ2.xls'

f101 = pd.read_excel(xl_filename, 'conto')
f101 = flatten(f101, 'conto')  
f101.set_index('conto').sort_values('dt').to_excel("summ2_f101_flat.xls")

bal = pd.read_excel(xl_filename, 'balance')
bal = flatten(bal, 'line')  
bal.set_index('line').sort_values('dt').to_excel("summ2_balance_flat.xls")
