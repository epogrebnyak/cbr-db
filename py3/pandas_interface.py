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
    tempdf = balancedf.reset_index()
    a = tempdf[tempdf['line']==198000]
    b = tempdf[tempdf['line']==298000]
    
    #merge dataframes
    saldo = a.merge(b, on=['dt', 'regn'], how='left', suffixes=('_a', '_b'))    
    
    #assign values to iv, ir and itogo as per the cases
    saldo_ext = pd.DataFrame(np.zeros((saldo.shape[0],3)), 
                             columns=['ir', 'iv', 'itogo'])
    saldo_ext.index = saldo.index
    
    #set ir column values    
    for col in ['ir', 'iv']:
        cola = col+'_a'; colb = col+'_b'
        a_gt_b = saldo[cola] > saldo[colb]
        a_lt_b = saldo[cola] < saldo[colb]        
        saldo_ext.ix[a_gt_b, col] = (saldo.ix[a_gt_b,cola] - saldo.ix[a_gt_b, colb]).values
        saldo_ext.ix[a_lt_b, col] = (saldo.ix[a_lt_b,colb] - saldo.ix[a_lt_b, cola]).values
        
    #set itogo column values
    saldo_ext.ix[:,'itogo'] = (saldo_ext.ix[:,'ir'] + saldo_ext.ix[:, 'iv']).values

    
    #select relevant columns from saldo
    #TODO: 
    
    #groupby 
    #TODO: 
    
    #delete rows from balacedf for lines 198K and 298K
    tempdf = tempdf[tempdf.line != 198000]
    tempdf = tempdf[tempdf.line != 298000]
    
    #insert rows in balancedf using saldo dataframe
    #TODO:
    
    return balancedf


def insert_totals(balancedf):
    '''
    Pandas equivalent to balance_make_insert_totals sql procedure.
    '''
    #TODO:
    pass


def init_balancedf():
    '''
    Initializes balance dataframe from alloc and f101 tables, 
    Equivalent to 'balance_make_step_1' sql procedure
    '''
    #left join alloc and f101 on 'conto' to create initial balance data frame
    balancedf = alloc.merge(f101, on='conto', how='left')    
    
    #drop rows with null conto values
    balancedf = balancedf[~balancedf['conto'].isnull()]
    
    #ir, iv, itogo multipy with mult
    balancedf['ir'] = balancedf['ir']*balancedf['mult']
    balancedf['iv'] = balancedf['iv']*balancedf['mult']
    balancedf['itogo'] = balancedf['itogo']*balancedf['mult']
    
    #groupby dt, line and regn and sum
    balancedf_grp = balancedf.groupby(['dt', 'line', 'regn'], sort=False)
    balancedf_grpdf = balancedf_grp.agg({'ir':sum,'iv':sum,'itogo':sum})
    
    #take relevant columns, la_p, ha_iv and lev
    balancedf = balancedf[['dt', 'line', 'regn', 'lev', 'la_p', 'has_iv']]
    
    #index on dt, line and regn
    balancedf = balancedf.set_index(keys=['dt', 'line', 'regn'])
    
    #add remaining columns from the grouped sum
    balancedf = balancedf.join(balancedf_grpdf)
    #TODO: check if we need to remove duplicates, need original sql balance table for that
    
    return balancedf


def make_balance():
    '''
    Pandas equivalent of make_balance procedure. It uses 'f101' and 'alloc' tables
    read from database to create 'balance' dataframe. 
    @return: 'balance' dataframe  
    '''
    #initialize balance dataframe from alloc and f101
    balancedf = init_balancedf()        
    
    #balance_make_saldo_198_298
    balancedf = insert_entries(balancedf)
    
    #balance_make_insert_totals
    balancedf = insert_totals(balancedf)
    
    return balancedf





