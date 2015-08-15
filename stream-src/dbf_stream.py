"""Access DBF files as stream and write to CSV."""

from common import change_extension, get_basename, dump_iter_to_csv, yield_csv_rows
from dbfread import DBF
from collections import OrderedDict

#______________________________________________________________________________
#
#  Access DBF files
#______________________________________________________________________________

# encoding of the dbf files
CODEPAGE = "cp866"

def open_dbf(f):
    return DBF(f, encoding=CODEPAGE)

def get_field_list(f):
    return [d.name for d in open_dbf(f).fields]
                
def dbf_stream(f):
    table = open_dbf(f)
    yield table.field_names
    for record in table:
        yield(list(record.values()))

def kill_itgap_row(gen):
    for row in gen:  
        if row[2] != "ITGAP":
            yield row
            
def write_to_csv(f, filter_func = kill_itgap_row):
    gen1 = dbf_stream(f)
    gen2 = filter_func(gen1)
    c = change_extension(f, "csv")
    dump_iter_to_csv(gen2, c)
    return c

#______________________________________________________________________________
#
#  Modify DBF data streams
#______________________________________________________________________________

def yield_csv_as_ordered_dict(f):
    gen = yield_csv_rows(f)
    field_names = next(gen)
    for row in gen:
        yield OrderedDict(zip(field_names, row)) 
    
NULL_CSV_MARKER = '0'
    
def mask_row(incoming_dict, field_names):     
    """Return OD with *field_names* as keys and *incoming_dict* as values, where matched."""
    row_dict = OrderedDict.fromkeys(field_names, NULL_CSV_MARKER)
    for k,v in incoming_dict.items():
        if k in field_names:
            row_dict[k] = v
    return row_dict

def yield_csv_subset(f, field_names):
    gen = yield_csv_as_ordered_dict(f)
    for row in gen:
         yield mask_row(row, field_names)




def get_csv_stream(f, field_names):
    сsv = write_to_csv(f)        
    return yield_csv_subset(сsv, field_names)
    

def yield_by_ts(ts, postfix= None, field_names = None):
        f = ts + postfix + ".dbf"
        return get_csv_stream(f, field_names)  
        
def yield_flat_stream(ts):
    # fi = "122012_B.DBF"    
    # fii = "122012B1.DBF"
  
        
    gen_i = yield_by_ts(ts, "_B", 
            ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'IR', 'IV', 'ITOGO', 'DT'])
    gen_ii = yield_by_ts(ts, "B1",
            ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'IR', 'IV',  'IITG', 'DT'])
    for row in gen_i:
        yield row 
    for row in gen_ii:
        yield row
        
if __name__ == "__main__":
    
   frm = [ # short table
          {'postfix' : "_B", 
        'field_names': ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'IR', 'IV', 'ITOGO', 'DT']}
          # long table
        , {'postfix' : "B1",
        'field_names': ['REGN', 'PLAN', 'NUM_SC', 'A_P', 'IR', 'IV',  'IITG', 'DT']}
        ]
        
   #for x in yield_by_ts("122012", **frm[1]):
   #             print(x)
                
                
   for i, x in enumerate(yield_flat_stream('122012')):
        print (x)
