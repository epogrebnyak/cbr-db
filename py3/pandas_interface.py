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


def insert_totals(balancedf):
    '''
    Pandas equivalent to balance_make_insert_totals sql procedure.
    '''
    #create balance total temporary dataframe
    btotal1 = balancedf.reset_index()
    btotal1 = btotal1[(btotal1.line!=100000) & (btotal1.la_p==1) & (btotal1.lev==10)]
    btotal1_grpdf = btotal1.groupby(['regn', 'dt']).agg({'ir':np.sum, 'iv':np.sum,
                                                       'itogo':np.sum, 
                                                       'line':lambda x:  100000,
                                                       'la_p':lambda x:  1,
                                                       'lev': lambda x:  1})
    #add has_iv column
    xx = btotal1.set_index(['regn', 'dt'])['has_iv']
    xx = xx.reset_index().drop_duplicates()
    xx = xx.set_index(['regn', 'dt'])
    btotal1_grpdf = pd.tools.merge.concat([btotal1_grpdf, xx], axis=1) 
    
    #add rows for line 200000 into balance total temprorary dataframe
    btotal2 = balancedf.reset_index()
    btotal2 = btotal2[(btotal2.line!=200000) & (btotal2.la_p==2) & (btotal2.lev==10)]
    btotal2_grpdf = btotal2.groupby(['regn', 'dt']).agg({'ir':np.sum,'iv':np.sum,
                                                      'itogo':np.sum,
                                                      'line':lambda x:  200000,
                                                      'la_p':lambda x:  2,
                                                      'lev': lambda x:  1})
    #add has_iv column
    xx = btotal1.set_index(['regn', 'dt'])['has_iv']
    xx = xx.reset_index().drop_duplicates()
    xx = xx.set_index(['regn', 'dt'])
    btotal2_grpdf = pd.tools.merge.concat([btotal2_grpdf, xx], axis=1) 
    
    #create final balance total dataframe
    btotal = pd.concat([btotal1_grpdf, btotal2_grpdf])
    
    #create balance net temporary dataframe
    bnet_tmp = btotal.reset_index()
    b = bnet_tmp[bnet_tmp.line == 100000] 
    z = bnet_tmp[bnet_tmp.line == 200000]     
    bnet = b.merge(z, on=['dt', 'regn'], how='left', suffixes=('_b','_z'))
    bnet = bnet.set_index(['dt', 'regn']) #i.e. groupby 
    for col in ['ir', 'iv', 'itogo']:
        bnet[col] = bnet[col+'_b'] - bnet[col+'_z']
    bnet['has_iv'] = bnet['has_iv_b']
    bnet['line'] = 500; bnet['lev'] = 1; bnet['la_p'] = 0    
    bnet = bnet[['ir', 'iv', 'itogo', 'line', 'lev', 'la_p', 'has_iv']]
    
    #insert rows from bnet and btotal into balance dataframe
    balancedf = pd.tools.merge.concat([balancedf, 
                                       btotal.reset_index().set_index(['dt', 'line', 'regn']), 
                                       bnet.reset_index().set_index(['dt', 'line', 'regn'])], 
                                      axis=0)
    return balancedf
    

def insert_entries(balancedf):
    '''
    pandas equivalent of sql procedure balance_make_saldo_198_298 
    '''
    #subset dataframes
    tempdf = balancedf.reset_index()
    a = tempdf[tempdf['line']==198000]
    b = tempdf[tempdf['line']==298000]
    
    #merge dataframes
    join_cols = ['dt', 'regn']
    saldo = a.merge(b, on=join_cols, how='left', suffixes=('_a', '_b'))    
    
    #assign values to iv, ir and itogo as per the cases    
    cols = ['line', 'lev', 'la_p', 'has_iv']
    saldo_a = pd.DataFrame(np.zeros((saldo.shape[0],9), dtype=np.int), 
                             columns=cols+join_cols+['ir', 'iv', 'itogo'])
    saldo_a.index = saldo.index
    
    saldo_b = pd.DataFrame(np.zeros((saldo.shape[0],9), dtype=np.int), 
                             columns=cols+join_cols+['ir', 'iv', 'itogo'])
    saldo_b.index = saldo.index
    
    #set ir column values    
    for col in ['ir', 'iv']:
        cola = col+'_a'; colb = col+'_b'
        a_gt_b = saldo[cola] > saldo[colb]
        a_lt_b = saldo[cola] < saldo[colb]        
        saldo_a.ix[a_gt_b, col] = (saldo.ix[a_gt_b,cola] - saldo.ix[a_gt_b, colb]).values
        saldo_b.ix[a_lt_b, col] = (saldo.ix[a_lt_b,colb] - saldo.ix[a_lt_b, cola]).values
        
    #set itogo column values
    saldo_a.ix[:,'itogo'] = (saldo_a.ix[:,'ir'] + saldo_a.ix[:, 'iv']).values
    saldo_b.ix[:,'itogo'] = (saldo_b.ix[:,'ir'] + saldo_b.ix[:, 'iv']).values

    #set other columns of a and b
    saldo_a.ix[:, join_cols] = saldo.ix[:, join_cols].values
    saldo_b.ix[:, join_cols] = saldo.ix[:, join_cols].values
    saldo_a.ix[:, cols] = saldo.ix[:, [c+'_a' for c in cols]].values
    saldo_b.ix[:, cols] = saldo.ix[:, [c+'_b' for c in cols]].values
    
    #groupby 
    saldo_a = saldo_a.set_index(['dt', 'line', 'lev', 'la_p', 'regn'])
    saldo_b = saldo_b.set_index(['dt', 'line', 'lev', 'la_p', 'regn']) 
    
    #UNION ALL
    saldo_ab = pd.concat([saldo_a, saldo_b]) #Note : this will keep duplicate rows
    saldo_ab = saldo_ab.reset_index()
    saldo_ab = saldo_ab.set_index(['dt', 'line', 'regn']) #set index same as balancedf index 
    
    #delete rows from balacedf for lines 198K and 298K
    tempdf = tempdf[tempdf.line != 198000]
    tempdf = tempdf[tempdf.line != 298000]
    balancedf = tempdf.set_index(['dt', 'line', 'regn'])
    
    #insert rows in balancedf using saldo_ab dataframe
    balancedf = pd.concat([balancedf, saldo_ab])
    
    return balancedf


def init_balancedf():
    '''
    Initializes balance dataframe from alloc and f101 tables, 
    Equivalent to 'balance_make_step_1' sql procedure
    '''
    
    #left join alloc and f101 on 'conto' to create initial balance data frame
    allocdf = alloc[~alloc['conto'].isnull()] #exclude rows where account is null
    joineddf = allocdf.merge(f101, on='conto', how='left')
    
    #ir, iv, itogo multipy with mult
    joineddf['ir'] = joineddf['ir']*joineddf['mult']
    joineddf['iv'] = joineddf['iv']*joineddf['mult']
    joineddf['itogo'] = joineddf['itogo']*joineddf['mult']
    
    #groupby dt, line and regn and sum
    grpdf = joineddf.groupby(['dt', 'line', 'regn']).agg({'ir':np.sum,'iv':np.sum, 'itogo':np.sum})
    
    #take other relevant columns, la_p, ha_iv and lev from joined dataframe i.e. joineddf
    joineddf = joineddf.set_index(keys=['dt', 'line', 'regn'])    
    joineddf = joineddf[['lev', 'la_p', 'has_iv']]
    joineddf = joineddf.reset_index().drop_duplicates().dropna()
    joineddf = joineddf.set_index(keys=['dt', 'line', 'regn'])
    
    #assign columns to balancedf
    balancedf = pd.tools.merge.concat([grpdf, joineddf], axis=1)
    
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
