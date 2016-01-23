from datetime import date

import pytest

from cbr_db.bankform import get_date_range_from_command_line,\
    get_date_endpoints


def test_get_date_range_from_command_line_101():
    args1 = {
        'pass': True,
        '<form>': '101',
        '<timestamp1>': '2005-01',
        '<timestamp2>': '2005-05',
        '--all-dates': False
    }

    assert (list(get_date_range_from_command_line(args1)) ==
            ['2005-01-01', '2005-02-01', '2005-03-01', '2005-04-01', '2005-05-01'])

    args2 = {
        'pass': True,
        '<form>': '101',
        '<timestamp1>': '2004-10',
        '<timestamp2>': '2005-02',
        '--all-dates': False
    }

    assert (list(get_date_range_from_command_line(args2)) ==
            ['2004-10-01', '2004-11-01', '2004-12-01', '2005-01-01', '2005-02-01'])

    args3 = {
        '<form>': '101',
        '<timestamp1>': None,
        '<timestamp2>': None,
        '--all-dates': False
    }

    assert get_date_range_from_command_line(args3) is None


def test_get_date_range_from_command_line_102():
    args1 = {
        'pass': True,
        '<form>': '102',
        '<timestamp1>': '2004q3',
        '<timestamp2>': '1q2005',
        '--all-dates': False
    }

    assert (list(get_date_range_from_command_line(args1)) ==
            ['2004-10-01', '2005-01-01', '2005-04-01'])

    args2 = {
        'pass': True,
        '<form>': '102',
        '<timestamp1>': '2004-02',
        '<timestamp2>': '2004-11',
        '--all-dates': False
    }

    assert (list(get_date_range_from_command_line(args2)) ==
            ['2004-04-01', '2004-07-01', '2004-10-01'])

    args3 = {
        'pass': True,
        '<form>': '102',
        '<timestamp1>': '2013',
        '<timestamp2>': '2014',
        '--all-dates': False
    }

    assert (list(get_date_range_from_command_line(args3)) ==
            ['2013-04-01', '2013-07-01', '2013-10-01', '2014-01-01',
             '2014-04-01', '2014-07-01', '2014-10-01', '2015-01-01'])

    args4 = {
        'pass': True,
        '<form>': '102',
        '<timestamp1>': '2013q1',
        '<timestamp2>': '4q2014',
        '--all-dates': False
    }

    assert (list(get_date_range_from_command_line(args4)) ==
            ['2013-04-01', '2013-07-01', '2013-10-01', '2014-01-01',
             '2014-04-01', '2014-07-01', '2014-10-01', '2015-01-01'])


@pytest.mark.parametrize('today,args,start_date,end_date', [
    (date(2015, 5, 15), {
        '<form>': '101',
        '--all-dates': True,
        '<timestamp1>': None,
        '<timestamp2>': None,
    }, date(2004, 2, 1), date(2015, 5, 1)),
    (date(2015, 5, 15), {
        '<form>': '101',
        '--all-dates': True,
        '<timestamp1>': '2015-03-15',
        '<timestamp2>': '2015-04-15',
    }, date(2015, 3, 1), date(2015, 4, 1)),
])
def test_get_date_endpoints(mocker, today, args, start_date, end_date):
    mock = mocker.patch('cbr_db.bankform.date')
    mock.side_effect = lambda *args, **kw: date(*args, **kw)
    mock.today = lambda *x: today
    assert get_date_endpoints(args) == (start_date, end_date)

