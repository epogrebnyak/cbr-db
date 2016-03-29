def import_alloc(xl_filename, sheet='alloc'):
     """Import dataframe"""
     pass    

def import_balance(xl_filename, sheet='balance'):
     """Import dataframe"""
     pass    

def import_contos(xl_filename, sheet='conto'):
     """Import dataframe"""
     pass  

def make_balance(f101, alloc):
    # for algorithm see sheet 'comment' in 'summ2.xls' 
    # https://github.com/epogrebnyak/cbr-db/blob/pandas/py3/pandas_interface.py#L177-L235
    pass
     
def comp(df1, df2):
     """Compare two dataframes assuming irregularities in row order"""
     return True

def balance_file_test(filename):
    alloc = import_alloc(filename)    
    f101 = import_contos(filename)
    ref_balance = import_balance(filename)
     
    balance = male_balance(alloc, conto)
    assert comp(df1=ref_balance, df2=balance)
     
if __name__ == "__main__":
    filename = 'summ2.xls'
    
    alloc = import_alloc(filename)
    f101 = import_contos(filename)
    ref_balance = import_balance(filename)
    # dataframes imported - intermediate result above
    
    balance = male_balance(alloc, conto)
    assert comp(df1=ref_balance, df2=balance)
    # final result 1 above
    
    balance_file_test("summ.xls")
    # final result 2 above
