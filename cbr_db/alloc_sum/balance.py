import pandas as pd
import numpy as np

REGN = 1010

def flatten(source_df, key_col):    
    col_dict  = {	
    # '2010-01-01' : [2009,	'2009_ir',	'2009_iv'],
	# '2011-01-01' : [2010,	'2010_ir',	'2010_iv'],
	# '2012-01-01' : [2011,	'2011_ir',	'2011_iv'],
	# '2013-01-01' : [2012,	'2012_ir',	'2012_iv'],
	# '2014-01-01' : [2013,	'2013_ir',	'2013_iv'],
	  '2015-01-01' : [2014,	'2014_ir',	'2014_iv'],
	# '2015-04-01' : ['20150401',	'20150401_ir',	'20150401_iv'],
	# '2015-05-01' : ['20150501',	'20150501_ir',	'20150501_iv'],
	# '2015-07-01' : ['20150701',	'20150701_ir',	'20150701_iv'],
	# '2015-08-01' : ['20150801',	'20150801_ir',	'20150801_iv'],
	# '2015-09-01' : ['20150901',	'20150901_ir',	'20150901_iv'],
	# '2015-10-01' : ['20151001',	'20151001_ir',	'20151001_iv'],
	# '2015-11-01' : ['20151101',	'20151101_ir',	'20151101_iv'],
	# '2015-12-01' : ['20151201',	'20151201_ir',	'20151201_iv'],
	  '2016-01-01' : ['20160101',	'20160101_ir',	'20160101_iv'] }
    
    df = pd.DataFrame()
    for dt, cols in col_dict.items():       
        df_block = source_df[[key_col] + cols]
        df_block ['dt'] = dt
        df_block = df_block.rename(index=str, columns={cols[0]:'itogo', cols[1]:'ir', cols[2]:'iv'})
        df = df.append(df_block)
    df['regn'] = REGN 
    return df   
    

def xl_import(xl_filename):
    alloc = pd.read_excel(xl_filename, 'alloc')
    f101 = pd.read_excel(xl_filename, 'conto')
    balance = pd.read_excel(xl_filename, 'balance')
    return (alloc, 
            flatten(f101, 'conto'),
            flatten(balance , 'line')) 

def make_balance(f101, alloc):
    joined = alloc.merge(f101, on='conto', how='left')
    
    # ir, iv, itogo multipied by *mult*
    joined['ir'] = joined['ir']*joined['mult']
    joined['iv'] = joined['iv']*joined['mult']
    joined['itogo'] = joined['itogo']*joined['mult']

    # 'as_index = False' allows flat structure without MultiIndex
    return joined.groupby(['dt', 'line', 'regn'], as_index = False).agg({'ir':np.sum,'iv':np.sum, 'itogo':np.sum})

     
def comp(df1, df2):
     """Compare two dataframes assuming irregularities in row order"""
     return True

def balance_file_test(filename):
    alloc, conto, ref_balance = xl_import(filename)   
    balance = make_balance(alloc, conto)
    assert comp(df1=ref_balance, df2=balance)
     
if __name__ == "__main__":

    alloc, f101, ref_balance = xl_import('summ2.xls')
    
    # Replicating SQL code below
    # see also sheet 'comment' in 'summ2.xls' 
    # and https://github.com/epogrebnyak/cbr-db/blob/pandas/py3/pandas_interface.py#L177-L235
    '''    
    SELECT  dt, line,
            regn,
            sum(   ir*mult) ir,
            sum(   iv*mult) iv,
            sum(itogo*mult) itogo
    from alloc a left join f101 v on v.conto = a.conto
    where v.conto is not null
    group by dt, line, regn;
    '''
    
    joined = alloc.merge(f101, on='conto', how='left')
    # todo 3 (optional): must check if there are any non-zero part of f101 that does not have code in alloc
    
    # ir, iv, itogo multipy with mult
    joined['ir'] = joined['ir']*joined['mult']
    joined['iv'] = joined['iv']*joined['mult']
    joined['itogo'] = joined['itogo']*joined['mult']

    # as_index = False allows flat structure - as in *ref_balance*
    balance = joined.groupby(['dt', 'line', 'regn'], as_index = False).agg({'ir':np.sum,'iv':np.sum, 'itogo':np.sum})
    
    def normalize(df):
        cols = ['regn', 'dt', 'line', 'ir', 'iv', 'itogo']
        sort_cols = ['regn', 'dt', 'line']
        return df.sort_values(sort_cols).reset_index()[cols]        
    
    balance = normalize(balance)
    ref_balance = normalize(ref_balance)
    
    # todo 2: check that values in *balance* and *ref_balance* are the same in corresponding rows and columns   
    print(balance.iloc[16,:] - ref_balance.iloc[16,:])
    
def comp(df1, df2):
    diff = df1
    for i, j in zip(df1.index, df1.columns):
        a1 = df1.loc[i,j]
        a2 = df2.loc[i,j]
        print(a1, a2)
        if a1 == a2:
            diff.loc[i,j] = True
        else:
            diff.loc[i,j] = (round(a1-a2, 2) == 0) 
            
    return (diff == True).all()
    
    #print (comp(balance, ref_balance))