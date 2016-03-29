import pandas as pd
import numpy as np

REGN = 1010
    
def flatten(source_df, key_col):    
    col_dict = {'2016-01-01':['20160101', '20160101_ir', '20160101_iv'],
                '2015-10-01':['20151001', '20151001_ir', '20151001_iv']}
                
    df = pd.DataFrame()
    for dt, cols in col_dict.items(): # '2016-01-01':             
        df_ = source_df[[key_col] + cols]
        df_['dt'] = dt
        df_ = df_.rename(index=str, columns={cols[0]:'itogo', cols[1]:'ir', cols[2]:'iv'})
        df = df.append(df_)
    df['regn'] = REGN 
    return df
    
def xl_import(xl_filename):
    alloc = pd.read_excel(xl_filename, 'alloc')
    f101 = pd.read_excel(xl_filename, 'conto')
    balance = pd.read_excel(xl_filename, 'balance')
    return (alloc, 
            flatten(f101, 'conto') 
            flatten(balance , 'line')) 

def make_balance(f101, alloc):
    pass
     
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

    grouped = joined.groupby(['dt', 'line', 'regn']).agg({'ir':np.sum,'iv':np.sum, 'itogo':np.sum})
    
    # todo 1: grouped has multiIndex, I want to have same flat structure as in *ref_balance*
    balance = grouped
    print(balance)
    print(ref_balance)
    
    # todo 2: check that values in *balance* and *ref_balance* are the same in corresponding rows and columns   