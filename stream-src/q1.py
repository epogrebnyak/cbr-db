# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 11:04:24 2015

@author: Евгений
"""


#cols = ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'VR', 'VV', 'VITG', 'ORA', 'OVA', 'OITGA', 'ORP', 'OVP', 'OITGP', 'IR', 'IV', 'IITG', 'DT', 'PRIZ']
#selection = ['REGN', 'PLAN', 'NUM_SC', 'ITOGO', 'A_P', 'DT']
#
#print([i for i, x in enumerate(cols) if x in selection])

from common import yield_csv_rows
from collections import OrderedDict

def yield_csv_as_ordered_dict(f):
    gen = yield_csv_rows(f)
    field_names = next(gen)
    for row in gen:
        yield OrderedDict(zip(field_names, row)) 
    
def mask_row(incoming_dict, field_names):    
    row = OrderedDict.fromkeys(field_names, 0)
    for k,v in incoming_dict.items():
        if k in field_names:
            row[k] = v
    return row 

def incoming_iter():
    yield OrderedDict([('NUM_SC', 1000),('A_P',1)]) 

def test_yield_by_selection(f):
    for x in yield_fieldnames_from_csv(f, ["NUM_SC", "SOME_EXTRA"]):
        print (x)    

def yield_fieldnames_from_csv(f, field_names):
    gen = yield_csv_as_ordered_dict(f)
    for row in gen:
         yield mask_row(row, field_names)
    
f = "122012_B.CSV"
test_yield_by_selection(f)
        
    