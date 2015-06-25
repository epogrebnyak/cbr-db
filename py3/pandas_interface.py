# 
# 2015-06-19 10:27 AM
# Pandas MySQL example 
# 
# http://pandas.pydata.org/pandas-docs/stable/io.html#excel-files
# https://pandas-docs.github.io/pandas-docs-travis/generated/pandas.read_sql_table.html#pandas.read_sql_table
# 

import pandas as pd
import numpy as np
import os
from pprint import pprint
from sqlalchemy import create_engine
from global_ini import DB_NAMES
import time

def get_sqla_connection():
    db_name = DB_NAMES['final']
    user = 'test_user'
    pwd = 'test_password'
    con = create_engine("mysql+pymysql://{0}:{1}@localhost/{2}".format(user, pwd, db_name))
    return con
    

start_time = time.time()
con = get_sqla_connection()

# Read datasets as dataframes
f101 = pd.read_sql_table('f101', con)
alloc = pd.read_sql_table('alloc', con)
balance = pd.read_sql_table('balance', con)

print("Datasets loaded in %f seconds" % (time.time() - start_time))


def insert_entries(balancedf):
    '''
    pandas equivalent of sql procedure balance_make_saldo_198_298 
    '''
    #subset dataframes
    a = balancedf[balancedf['line']==198000]
    b = balancedf[balancedf['line']==298000]
    
    #merge dataframes
    saldo = a.merge(b, on=['dt', 'regn'], how='left')    
    
    #assign values to iv, ir and itogo as per the cases
    saldo_ext = pd.DataFrame(np.zeros(saldo.shape[0],3), 
                             columns=['ir', 'iv', 'itogo'])
    saldo_ext.index = saldo.index
    
    #set ir column values
    saldo_ext.ix[saldo['ir_x'] > saldo['ir_y'],'ir'] = (saldo.ix[saldo['ir_x'] > saldo['ir_y'],'ir_x'] - saldo.ix[saldo['ir_x'] > saldo['ir_y'],'ir_y']).values
    saldo_ext.ix[saldo['ir_x'] < saldo['ir_y'],'ir'] = (saldo.ix[saldo['ir_x'] < saldo['ir_y'],'ir_y'] - saldo.ix[saldo['ir_x'] < saldo['ir_y'],'ir_x']).values
    
    #set iv column values
    saldo_ext.ix[saldo['iv_x'] > saldo['iv_y'],'iv'] = (saldo.ix[saldo['iv_x'] > saldo['iv_y'],'iv_x'] - saldo.ix[saldo['iv_x'] > saldo['iv_y'],'iv_y']).values
    saldo_ext.ix[saldo['iv_x'] < saldo['iv_y'],'iv'] = (saldo.ix[saldo['iv_x'] < saldo['iv_y'],'iv_y'] - saldo.ix[saldo['iv_x'] < saldo['iv_y'],'iv_x']).values
    
    #set itogo column values
    saldo_ext.ix[:,'itogo'] = (saldo_ext.ix[:,'ir'] + saldo_ext.ix[:, 'iv']).values

    #stack saldo_ext to saldo i.e. add ir, iv and itogo updated columns
    saldo = pd.tools.merge.concat([saldo, saldo_ext], axis=1)
    
    #select relevant columns from saldo
    #TODO: 
    
    #groupby 
    #TODO: 
    
    #delete rows from balacedf for lines 198K and 298K
    balancedf = balancedf[balancedf.line != 198000]
    balancedf = balancedf[balancedf.line != 298000]
    
    #insert rows in balancedf using saldo dataframe
    #TODO:
    
    return balancedf


def insert_totals(balancedf):
    '''
    Pandas equivalent to balance_make_insert_totals sql procedure.
    '''
    #TODO:
    pass


def make_balance():
    '''
    Pandas equivalent of make_balance procedure. It uses 'f101' and 'alloc' tables
    read from database to create 'balance' dataframe. 
    @return: 'balance' dataframe  
    '''
    #left join alloc and f101 on 'conto' to create initial balance data frame
    balancedf = alloc.merge(f101, on='conto', how='left')    
    #TODO: check if v.conto is null, if yes then drop those rows, need some data in tables for this
    #TODO: groupby and aggregate
    balancedf = balancedf.ix[:,['dt', 'line', 'lev', 'la_p', 'regn', 'has_iv', 
                                'ir', 'iv', 'itogo']]
    
    
    #balance_make_saldo_198_298
    balancedf = insert_entries(balancedf)
    
    #balance_make_insert_totals
    balancedf = insert_totals(balancedf)
    

    return balancedf



for var in [f101, alloc, balance]:
    print()
    print(var.head())
    pprint(var.columns.tolist())





