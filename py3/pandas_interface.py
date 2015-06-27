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
    if(btotal1.shape[0] > 0):
        btotal1['line'] = 100000; btotal1['lev'] = 1; btotal1['la_p'] = 1
    btotal_grpdf = btotal1.groupby(['regn', 'dt']).agg({'ir':np.sum,
                                                       'iv':np.sum,
                                                       'itogo':np.sum})
    btotal1 = btotal1.drop(['ir', 'iv', 'itogo'], axis=1)
    btotal1 = btotal1.set_index(['regn', 'dt'])
    btotal1 = btotal1.join(btotal_grpdf)
    
    #add rows for line 200000 into balance total temprorary dataframe
    btotal2 = balancedf.reset_index()
    btotal2 = btotal2[(btotal2.line!=200000) & (btotal2.la_p==2) & (btotal2.lev==10)]
    if(btotal2.shape[0]>0):
        btotal2['line'] = 200000; btotal2['lev'] = 1; btotal2['la_p'] = 2
    bnet_grpdf = btotal2.groupby(['regn', 'dt']).agg({'ir':np.sum,
                                                   'iv':np.sum,
                                                   'itogo':np.sum})
    btotal2 = btotal2.drop(['ir', 'iv', 'itogo'], axis=1)
    btotal2 = btotal2.set_index(['regn', 'dt'])
    btotal2 = btotal2.join(bnet_grpdf)
    
    #create final balance total dataframe
    btotal = pd.concat([btotal1, btotal2])
    
    #create balance net temporary dataframe
    bnet_tmp = btotal.reset_index()
    b = bnet_tmp[bnet_tmp.line == 100000] 
    z = bnet_tmp[bnet_tmp.line == 200000]
    bnet_tmp = b.merge(z, on=['dt', 'regn'], how='left', suffixes=('_b','_z'))
    bnet = pd.DataFrame()
    bnet['ir'] = bnet_tmp['ir_b'] - bnet_tmp['ir_z']
    bnet['iv'] = bnet_tmp['iv_b'] - bnet_tmp['iv_z']
    bnet['itogo'] = bnet_tmp['itogo_b'] - bnet_tmp['itogo_z']
    bnet['dt'] = bnet_tmp['dt']; bnet['regn'] = bnet_tmp['regn']
    for col in ['has_iv', 'line', 'lev', 'la_p']:
        bnet[col] = bnet_tmp[col+'_b']
    bnet['line'] = 500; bnet['lev'] = 1; bnet['la_p'] = 0
    bnet = bnet.set_index(['regn', 'dt'])
    
    #insert rows from bnet and btotal into balance dataframe
    balancedf = balancedf.reset_index()
    balancedf = balancedf.set_index(['regn', 'dt'])
    balancedf = pd.tools.merge.concat([balancedf, btotal, bnet], axis=0)
    #set original indexing of balance dataframe
    balancedf = balancedf.reset_index()
    balancedf = balancedf.set_index(['dt', 'line', 'regn'])
    balancedf = balancedf.drop_duplicates()
    
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
    saldo_a = pd.DataFrame(np.zeros((saldo.shape[0],9)), 
                             columns=cols+join_cols+['ir', 'iv', 'itogo'])
    saldo_a.index = saldo.index
    
    saldo_b = pd.DataFrame(np.zeros((saldo.shape[0],9)), 
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
    
    #drop duplicates
    balancedf = balancedf.drop_duplicates() 
    
    return balancedf


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
    
    #drop duplicates 
    balancedf = balancedf.drop_duplicates()
    
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





