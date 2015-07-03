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


def get_balance_total(balancedf, line, la_p):
    '''
    A utitility function. Returns balance  dataframe for given line and la_p values, grouped by
    'regn' and 'dt
    '''
    btotal = balancedf.reset_index()
    btotal = btotal[(btotal.line!=line) & (btotal.la_p==la_p) & (btotal.lev==10)]
    btotal_grpdf = btotal.groupby(['regn', 'dt']).agg({'ir':np.sum, 'iv':np.sum,
                                                       'itogo':np.sum,
                                                       'line':lambda x:  line,
                                                       'la_p':lambda x:  la_p,
                                                       'lev': lambda x:  1})
    #add has_iv column
    # Need comment: why adding has_iv is important/difficult and requires 4 lines of code? is iv used anywhere in the code below?
    # comment: has_iv is present in sql table too so to be same as in database it has to be added.
    # I too was not sure if it is needed, but has to be aligned with sql tables, so added it.
    # I couldn't find a very effective way to do it using groupby operation above, as this column has
    # no reduce operation (sum, count, etc) assigned to it, so had to handled separately.
    xx = btotal.set_index(['regn', 'dt'])['has_iv']
    xx = xx.reset_index().drop_duplicates()
    xx = xx.set_index(['regn', 'dt'])
    btotal_grpdf = pd.tools.merge.concat([btotal_grpdf, xx], axis=1)

    return btotal_grpdf


def insert_totals(balancedf):
    '''
    Pandas equivalent to balance_make_insert_totals sql procedure.
    '''

    #  done todo:  creating 'btotal1_grpdf' and 'btotal2_grpdf' seems symmetric, make function get_balance_toal(balance_line, la_p) to avoid code duplication
    #  get_balance_toal(balance_line, la_p) must return btotal1_grpdf as in line 57

    #create balance total temporary dataframes
    btotal1_grpdf = get_balance_total(balancedf, line=100000, la_p=1)
    btotal2_grpdf = get_balance_total(balancedf, line=200000, la_p=2)

    #create final balance total dataframe
    # Need comment: what does pd.concat do? a union of the frames?
    # comment: yes, it is like UNION ALL operation with duplicate rows allowed,
    # by default it appends rows of passed dataframes i.e. axis=0
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

    # need comment: can reset_index().set_index be done before this statement?
    # comment: yes, it can be done.
    balancedf = pd.tools.merge.concat([balancedf,
                                       btotal.reset_index().set_index(['dt', 'line', 'regn']),
                                       bnet.reset_index().set_index(['dt', 'line', 'regn'])],
                                      axis=0)
    return balancedf


def insert_entries(balancedf):
    '''
    pandas equivalent of sql procedure balance_make_saldo_198_298
    '''
    #subset dataframes - work with lines 198000 and 298000

    tempdf = balancedf.reset_index()
    # not todo: rename 'a' and 'b'
    a = tempdf[tempdf['line']==198000]
    b = tempdf[tempdf['line']==298000]

    #merge dataframes
    # Need comment: what is _a, _b? how does that affect column names?
    # comment: when you join two dataframes with same columns, their column names
    # are suffixed to avoid naming conflicts in the joined dataframe.
    join_cols = ['dt', 'regn']
    saldo = a.merge(b, on=join_cols, how='left', suffixes=('_a', '_b'))

    #assign values to iv, ir and itogo as per the cases in sql query
    # todo: comment above unclear: cases refers to cases in sql code
    # Need comment: what is the intent of np.zeros((saldo.shape[0],9)
    # comment: it is a place holder for values of dataframe. Empty shape  of
    # dataframe is needed when you want to index a dataframe using 'ix' or 'iloc'
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
        # Need comment: what is .ix?
        # comment: .ix, .iloc, .loc is pandas way of indexing and selecting subsets from a dataframe
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
    # Need comment: why need reset and set index?
    # comment: because saldo_ab has index on ['dt', 'line', 'lev', 'la_p', 'regn'] but
    # balance table i.e. balance dataframe is indexed on ['dt', 'line', 'regn']
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
    Equivalent to 'balance_make_step_1' sql procedure:

    create table if not exists balance as
    SELECT  dt, line,
            lev, la_p,
            regn,
            has_iv,
            sum(   ir*mult) ir,
            sum(   iv*mult) iv,
            sum(itogo*mult) itogo
    from alloc a left join f101 v on v.conto = a.conto
    where v.conto Is not null
    group by dt, line, regn;

    '''

    #left join alloc and f101 on 'conto' to create initial balance data frame
    # Need comment: why apply this to 'alloc', not 'f101'?
    # comment: we are doing a left join on alloc, and this is how it is in sql code.
    # Need further comment: in sql code we have where v.conto Is not null and v is f101. (see line 191 above)
    # update: yes, you are right, it was a bug, now it is aligned with sql code.
    f101df = f101[~f101['conto'].isnull()] #exclude rows where account is null

    joineddf = alloc.merge(f101df, on='conto', how='left')

    #ir, iv, itogo multipy with mult
    joineddf['ir'] = joineddf['ir']*joineddf['mult']
    joineddf['iv'] = joineddf['iv']*joineddf['mult']
    joineddf['itogo'] = joineddf['itogo']*joineddf['mult']

    #groupby dt, line and regn and sum
    grpdf = joineddf.groupby(['dt', 'line', 'regn']).agg({'ir':np.sum,'iv':np.sum, 'itogo':np.sum})

    #take other relevant columns, la_p, ha_iv and lev from joined dataframe i.e. joineddf
    # Need comment: what is the role of .set_index, . reset_index?
    # comment: set_index is used to set multi-column indexing in pandas,
    # reset_index is to remove this indexing to access a single column if it was indexed.
    joineddf = joineddf.set_index(keys=['dt', 'line', 'regn'])
    # Need comment: what is hapenning to joineddf in line below? reducing all of joineddf to three columns?
    # comment:  since we need only 9 columns from joined df, and out of these 9, three are used to index it,
    # by default a pandas join operation will have duplicate rows, so final dataframe should remove these duplicates.
    joineddf = joineddf[['lev', 'la_p', 'has_iv']]
    joineddf = joineddf.reset_index().drop_duplicates().dropna()
    joineddf = joineddf.set_index(keys=['dt', 'line', 'regn'])
    #assign columns to balancedf
    # Need comment: what is axis = 1?
    # comment: axis={0,1}, 0 means x-axis and 1 means y-axis. Here axis=1 means we
    # want to stack columns of dataframes to get a new dataframe with all the columns.
    # Need comment: we are efffectively making two dataframes and joining them together to get 'balancedf'
    #               can there be a different startegy or is this the only way to implement?
    # comment: There is one other strategy, but will have to try it and see if it works, using solely groupby operation.
    # update: tried other strategy with "apply" function on groupby frame, but apply doesn't function on
    # multiple columns, thus will lead to same amount of code.
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
