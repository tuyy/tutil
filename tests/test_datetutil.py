# -*- codnig: utf-8 -*-

"""test tutil.dateutil

copyright: (c) 2020 tuyy
license: MIT, see LICENSE for more details.
"""

from datetime import date

from pytest import raises  # type: ignore

from tutil.dateutil import *
from tutil.functional import *


def test_DateRangeIterator():
    result = go(
        DateRangeIterator(date(2020, 5, 24), date(2020, 5, 28), 2),
        t_map(lambda d: str(d)),
        list,
    )
    assert ["2020-05-24", "2020-05-26", "2020-05-28"] == result


def test_DateRangeIterator_twice_call():
    it = DateRangeIterator(date(2020, 5, 24), date(2020, 5, 28), 2)
    first_iterator = list(it)
    second_iterator = list(it)
    assert first_iterator == second_iterator


def test_DateRangeIterator_invalid_dates():
    start_date = date(2020, 5, 24)
    end_date = date(2020, 5, 20)

    with raises(ValueError):
        DateRangeIterator(start_date, end_date)

    date_iterator = DateRangeIterator(date(2020, 5, 24), date(2020, 6, 1))
    with raises(ValueError):
        date_iterator.start_date = date(2020, 6, 2)

    with raises(ValueError):
        date_iterator.end_date = date(2020, 5, 23)


def test_DateRangeSequence():
    result = go(
        DateRangeSequence(date(2020, 5, 24), date(2020, 5, 28), 2),
        t_map(lambda d: str(d)),
        list,
    )
    assert ["2020-05-24", "2020-05-26", "2020-05-28"] == result
