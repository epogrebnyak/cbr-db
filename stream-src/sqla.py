# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 19:29:06 2015

@author: Евгений
"""

#    field_names_i  = ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'IR', 'IV', 'ITOGO', 'DT']
#    field_names_ii = ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'IR', 'IV',  'IITG', 'DT']
 
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, MetaData
from datetime import datetime

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///122012.sqlite3', echo=True)


metadata = MetaData()
f101 = Table('f101',   metadata,
       Column('regn',  Integer, primary_key=True),
       Column('plan',  String),
       Column('conto', Integer, primary_key=True),
       Column('a_p',   Integer),
       Column('ir',    Integer),
       Column('iv',    Integer),
       Column('itogo', Integer, primary_key=True),
       Column('dt',    Date,    primary_key=True)
       )

metadata.create_all(engine)        
       
from dbf_stream import yield_flat_stream

def get_date(isodate):
    return datetime.strptime(isodate, "%Y-%m-%d").date() 

def to_int(x):
    return int(float(x))     

def yield_dicts(ts):
    gen = yield_flat_stream(ts)
    for row in gen:
        row = [x for x in row.values()]
        yield {'regn': to_int(row[0]),
               'plan': row[1],
              'conto': to_int(row[2]),
                'a_p': to_int(row[3]),           
                 'ir': to_int(row[4]),
                 'iv': to_int(row[5]),
              'itogo': to_int(row[6]),
                 'dt': get_date(row[7])
               }
             
gen = yield_dicts('122012')
conn = engine.connect()
conn.execute(f101.insert(), [x for x in gen])


REPLACE [LOW_PRIORITY | DELAYED]
    [INTO] tbl_name [(col_name,...)]
    {VALUES | VALUE} ({expr | DEFAULT},...),(...),...
    
    
