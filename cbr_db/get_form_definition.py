import os
import datetime

from .date_engine import shift_month_ahead, date2iso, quarter2date


f101 = {
    'f101_private': {
        'tag': 'f101_B',
        'name': "bank accounts - short file",
        'postfix': "_B",
        'db_table': 'bulk_f101_b',
        'dbf_fields': ['DT', 'REGN', 'NUM_SC', 'A_P', 'ITOGO'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_B).DBF$"
    }
 }

def get_parent_dirname(path):
    """
    Returns 2013 for path = r"D:\git\cbr-data\data.private\101\txt\2013\f101_12.txt"
    """
    parent = os.path.dirname(path)    
    return int(os.path.split(parent)[1])

 
def decompose_private_txt_filename (path, form = '101'):
    basename = os.path.basename(path)    
    year = get_parent_dirname(path)
    if form == '101':
        # not-todo: this may be handled using regex 
        # reads from f101_01.txt, f101_12.txt         
        month = int(basename[5:6]) 
        isodate = date2iso(shift_month_ahead(datetime.date(year, month, 1)))        
    if form == '102':  
        # reads from f102_1.txt, f102_4.txt
        quarter = int(basename[5])
        isodate = date2iso(quarter2date(year, quarter))    
    return isodate        
        
        # todo: bulk_f101veb also is from config.
        # csv_file = os.path.join(csv_dir, "bulk_f101veb.{}".format(isodate))    
 
print(
    decompose_private_txt_filename(r"D:\git\cbr-data\data.private\101\txt\2013\f101_12.txt", '101')
  , decompose_private_txt_filename(r"D:\git\cbr-data\data.private\101\txt\2020\f102_4.txt", '102')
)



def f101_txt2csv(filename, year):
    """
    Special converter of form 101 text files to csv files.
    """
    csv_file = get_target_csv_path_form101(filename, csv_file)
    converter_f101_txt2csv(filename, csv_file)

def get_target_csv_path_form101(txt_path, year):

    csv_dir = get_private_data_folder('101', 'csv')    
    
    # todo: this should be handled using regex
    month = int(os.path.basename(filename)[5:7])
    
    isodate = date2iso(shift_month_ahead(datetime.date(year, month, 1)))

 
 
 