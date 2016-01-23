from datetime import date

import pytest

from cbr_db.utils import dates
from cbr_db.utils.dates import get_date


def test_get_date_fmt():
    test_strings = ['2005', '01.01.2005',  '1.1.2005', '1.2005', '2005-01',
                    '2005-01-01', '2004Q4', '4q2004']
    test_format = ['%Y', '%d.%m.%Y', '%d.%m.%Y', '%m.%Y', '%Y-%m',
                   '%Y-%m-%d', 'quarter', 'quarter']
    target_date = date(2005, 1, 1)

    for string, target_format in zip(test_strings, test_format):
        date_, format_ = get_date(string)
        assert date_ == target_date
        assert format_ == target_format


def test_get_date():
    assert get_date('1988')[0] == date(1988, 1, 1)
    assert get_date('03.12.2015')[0] == date(2015, 12, 3)
    assert get_date('2.2000')[0] == date(2000, 2, 1)
    assert get_date('12.2030')[0] == date(2030, 12, 1)
    assert get_date('2015-01-05')[0] == date(2015, 1, 5)
    assert get_date('1977-12')[0] == date(1977, 12, 1)
    assert get_date('1Q1988')[0] == date(1988, 4, 1)
    assert get_date('2014q1')[0] == date(2014, 4, 1)
    assert get_date('2014q2')[0] == date(2014, 7, 1)
    assert get_date('2014q3')[0] == date(2014, 10, 1)
    assert get_date('2014q4')[0] == date(2015, 1, 1)


def test_shift_month_ahead():
    assert dates.shift_month_ahead(date(2015, 5, 1)) == date(2015, 6, 1)

    assert dates.shift_month_ahead(date(2012, 12, 1)) == date(2013, 1, 1)

    with pytest.raises(ValueError):
        dates.shift_month_ahead(date(2013, 3, 31))


def test_shift_month_behind():
    assert dates.shift_month_behind(date(2015, 12, 1)) == date(2015, 11, 1)
    
    assert dates.shift_month_behind(date(1988, 7, 1)) == date(1988, 6, 1)

    assert dates.shift_month_behind(date(2012, 1, 1)) == date(2011, 12, 1)

    with pytest.raises(ValueError):
        dates.shift_month_behind(date(2013, 3, 31))


def test_shift_month_to_quarter_start():
    for month in range(1, 4):
        assert dates.shift_month_to_quarter_start(month) == 1

    for month in range(4, 7):
        assert dates.shift_month_to_quarter_start(month) == 4

    for month in range(7, 10):
        assert dates.shift_month_to_quarter_start(month) == 7

    for month in range(10, 13):
        assert dates.shift_month_to_quarter_start(month) == 10


def test_get_date_range():
    assert (dates.get_date_range(date(2012, 3, 1), date(2012, 5, 1)) ==
            [date(2012, 3, 1), date(2012, 4, 1), date(2012, 5, 1)])

    assert (dates.get_date_range(date(1988, 11, 1), date(1989, 1, 1)) ==
            [date(1988, 11, 1), date(1988, 12, 1), date(1989, 1, 1)])


def test_zero_padded_month():
    assert dates.zero_padded_month(5) == "05"
    assert dates.zero_padded_month(11) == "11"


def test_datetime2iso():
    assert dates.date2iso(date(1988, 1, 1)) == '1988-01-01'
    assert dates.date2iso(date(2015, 5, 23)) == '2015-05-23'


def test_iso2date():
    assert dates.iso2date('1988-01-01') == date(1988, 1, 1)
    assert dates.iso2date('2015-05-23') == date(2015, 5, 23)


def test_date2timestamp():
    assert dates.date2timestamp(101, date(2014, 5, 3)) == '042014'
    assert dates.date2timestamp('101', date(2014, 1, 5)) == '122013'


def test_isodate2timestamp():
    assert dates.isodate2timestamp(101, '2014-05-03') == '042014'

    assert dates.isodate2timestamp('101', '2014-01-05') == '122013'


def test_quarter2date():
    assert dates.quarter2date(2000, 1) == date(2000, 4, 1)
    assert dates.quarter2date(2000, 2) == date(2000, 7, 1)
    assert dates.quarter2date(2000, 3) == date(2000, 10, 1)
    assert dates.quarter2date(2000, 4) == date(2001, 1, 1)


def test_date2quarter():
    assert dates.date2quarter(date(2000, 4, 1)) == (2000, 1)
    assert dates.date2quarter(date(2000, 7, 1)) == (2000, 2)
    with pytest.raises(ValueError):
        dates.date2quarter(date(2000, 9, 1))
    assert dates.date2quarter(date(2000, 10, 1)) == (2000, 3)
    with pytest.raises(ValueError):
        dates.date2quarter(date(2000, 11, 1))
    with pytest.raises(ValueError):
        dates.date2quarter(date(2000, 12, 1))
    assert dates.date2quarter(date(2001, 1, 1)) == (2000, 4)


def test_conv_date2quarter():
    assert dates.conv_date2quarter('2015-01-01') == (2014, 4)
    assert dates.conv_date2quarter('2015-03-01') == (2015, 1)
    assert dates.conv_date2quarter('2015-04-01') == (2015, 1)
    assert dates.conv_date2quarter('2015-06-01') == (2015, 2)
    assert dates.conv_date2quarter('2015-09-01') == (2015, 3)
    assert dates.conv_date2quarter('2015-12-01') == (2015, 4)


def test_current_year():
    assert dates.get_current_year() == date.today().year


def test_get_date_from_quarter_string():
    assert (dates.get_date_from_quarter_string("2000q1") ==
            (date(2000, 4, 1), "quarter"))
    assert (dates.get_date_from_quarter_string("2000q4") ==
            (date(2001, 1, 1), "quarter"))


def test_get_next_quarter_end_date():
    assert dates.get_next_quarter_end_date(date(2003, 1, 1)) == date(2003, 1, 1)

    for month in range(2, 5):
        assert dates.get_next_quarter_end_date(date(2003, month, 1)) == date(2003, 4, 1)

    for month in range(5, 8):
        assert dates.get_next_quarter_end_date(date(2003, month, 1)) == date(2003, 7, 1)

    for month in range(8, 11):
        assert dates.get_next_quarter_end_date(date(2003, month, 1)) == date(2003, 10, 1)

    for month in range(11, 12):
        assert dates.get_next_quarter_end_date(date(2003, month, 1)) == date(2004, 1, 1)


@pytest.mark.parametrize('form,today,dt,expected', [
    # Form 101
    ('101', date(2015, 5, 15), date(2014, 1, 1), date(2014, 12, 1)),
    ('101', date(2015, 5, 15), date(2015, 1, 1), date(2015, 5, 1)),
    ('101', date(2015, 5, 15), date(2016, 1, 1), date(2015, 5, 1)),
    # Form 102 - per quarter
    ('102', date(2015, 5, 15), date(2014, 1, 1), date(2015, 1, 1)),
    ('102', date(2015, 5, 15), date(2015, 1, 1), date(2015, 4, 1)),
    ('102', date(2015, 5, 15), date(2016, 1, 1), date(2015, 4, 1)),

])
def test_get_last_date_in_year(mocker, form, today, dt, expected):
    mock = mocker.patch('cbr_db.utils.dates.date')
    mock.side_effect = lambda *args, **kw: date(*args, **kw)
    mock.today = lambda *x: today
    assert dates.get_last_date_in_year(dt, form) == expected
