"""
Database names + credentials and form descriptions.

Todo: separate configparser.ConfigParser() and form decriptions in different files.

Contents of this file
   settings.py (new)         - reads with configparser.ConfigParser()  + database names + codepage
   form_definitions.py (new) - hardcoded form parameters + access functions

Must separate global_ini.py into two fils + change import dependencies in other project files.
Check with https://github.com/epogrebnyak/cbr-db/blob/master/cbr_db/script/test-one-date-101.bat

Not changed:
   config_folders.py
"""

import configparser

#############################################################################
# CONFIGURATION FILE
#############################################################################

config = configparser.ConfigParser()
config.read('../settings.cfg')

#############################################################################
# DATABASE NAMES
#############################################################################

DB_NAME_RAW = 'dbf_db'
DB_NAME_FINAL = 'cbr_db'
DB_NAMES = {'raw': DB_NAME_RAW, 'final': DB_NAME_FINAL}

#############################################################################
# FORM DESCRIPTIONS
#############################################################################

f101 = {
    'f101_B': {
        'tag': 'f101_B',
        'name': "bank accounts - short file",
        'postfix': "_B",
        'db_table': 'bulk_f101_b',
        'dbf_fields': ['DT', 'REGN', 'NUM_SC', 'A_P', 'ITOGO'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(_B).DBF$"
    },

    'f101B1': {
        'tag': 'f101B1',
        'name': "bank accounts - long file",
        'postfix': "B1",
        'db_table': 'bulk_f101b1',
        'dbf_fields': ['DT', 'REGN', 'NUM_SC', 'A_P', 'IR', 'IV', 'IITG'],
        'regex': r"^([0-9]{2})(20[0-9]{2})(B1).DBF$"
    }
}

f102 = {
    'f102_P': {
        'tag': 'f102_P',
        'name': "form 102 – short data",
        'postfix': "_P",
        'db_table': 'bulk_f102_P',
        'dbf_fields': ['DT', 'REGN', 'QUART', 'YEAR', 'CODE', 'ITOGO'],
        'regex': r"^([1-4])(20[0-9]{2})(_P).DBF$"
    },

    'f102P1': {
        'tag': 'f102_P1',
        'name': "form 102 – long data",
        'postfix': "_P1",
        'db_table': 'bulk_f102_P1',
        'dbf_fields': ['DT', 'REGN', 'QUART', 'YEAR', 'CODE', 'SIM_R', 'SIM_V', 'SIM_ITOGO'],
        'regex': r"^([1-4])(20[0-9]{2})(_P1).DBF$"
    }
}

FORM_DATA = {
    '101': f101,
    '102': f102
}


def get_private_data_param(form, tag):
    table_name_dict = {
        '101': {
            'db_table': 'bulk_f101_private'
        },
        '102': {
            'db_table': 'bulk_f102_private'
        }
    }
    return table_name_dict[form][tag]


def get_private_data_db_table(form):
    return get_private_data_param(form, 'db_table')


ACCOUNT_NAMES_DBF = {
    '101': 'NAMES.DBF',
    '102': 'SPRAV1.DBF'
}

ACCOUNT_TABLE_NAME = {
    '101': "plan",
    '102': "sprav102"
}

ACCOUNT_TABLE_FIELDS = {
    '101': ("PLAN", "CONTO", "NAME", "LEVEL"),
    '102': ("NOM", "PRSTR", "CODE", "NAME")
}

ACCOUNT_DBF_FIELDS = {
    '101': ("PLAN", "NUM_SC", "NAME", "TYPE"),
    '102': ("NOM", "PRSTR", "CODE", "NAME")
}


def get_account_name_parameters(form):
    return ACCOUNT_TABLE_NAME[form], ACCOUNT_TABLE_FIELDS[form], ACCOUNT_DBF_FIELDS[form]

# Bank names

BANK_NAMES_DBF = (
    "[0-1][0-9]{5}_N.DBF",
    "[0-1][0-9]{5}N1.DBF"
)
BANK_TABLE_NAME = "bank"
BANK_TABLE_FIELDS = [("regn", "regn_name"), ("regn", "regn_name")]
BANK_DBF_FIELDS = [("REGN", "NAME_B"), ("REGN", "NAME_B")]
