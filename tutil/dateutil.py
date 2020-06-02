# -*- coding: utf-8 -*-

"""
tutil.dateutil
~~~~~~~~~~~~~~

* DateRangeIterator

copyright: (c) 2020 tuyy
license: MIT, see LICENSE for more details.
"""

import datetime


class DateRangeIterator(object):
    """start_date 부터 end_date 까지 day 단위로 day_step 씩 순회하는 Iterator"""

    def __init__(self, start_date, end_date, day_step=1):
        """start_date 이상 end_date 이하 까지 day_step 씩 증가
        >>> for d in DateRangeIterator(start_date=date(2019, 5, 24),
                                       end_date=date(2019, 5, 28),
                                       day_step=2):
        ...     print(d)
        ...
        2019-05-24
        2019-05-26
        2019-05-28
        """

        self.start_date = start_date
        self.end_date = end_date
        self._day_step = day_step

    def __iter__(self):
        current_day = self.start_date
        while current_day <= self.end_date:
            yield current_day
            current_day += datetime.timedelta(days=self._day_step)

    @property
    def start_date(self):
        """입력으로 받은 start_date를 리턴"""
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        if hasattr(self, "_end_date") and start_date > self._end_date:
            raise ValueError("start_date is bigger than end_date.")

        self._start_date = start_date

    @property
    def end_date(self):
        """입력으로 받은 end_date를 리턴"""
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        if hasattr(self, "_start_date") and self._start_date > end_date:
            raise ValueError("start_date is bigger than end_date.")

        self._end_date = end_date
