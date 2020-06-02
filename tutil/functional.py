# -*- coding:utf-8 -*-

"""
tutil.functional
~~~~~~~~~~~~~~~~

* is_number, iterable, curry
* t_filter, t_map, reduce, reject, find, take, for_each, go

copyright: (c) 2020 tuyy
license: MIT, see LICENSE for more details.
"""

import sys
import functools
import inspect


if sys.version[0:3] == "2.7":
    from collections import Iterable

    inspect.getfullargspec = inspect.getargspec  # type: ignore
else:
    from collections.abc import Iterable


def is_number(val):
    """입력값 val 가 int형 변환이 가능하면 True, 아니면 False"""

    try:
        int(val)
    except TypeError:
        return False
    else:
        return True


def iterable(val):
    """입력값 val 가 iterable이면 True, 아니면 False"""

    return isinstance(val, Iterable)


def curry(func):
    """입력값 f를 curry하여 사용하기 위한 decorate 함수"""

    args_cnt = len(inspect.getfullargspec(func).args)
    default_args_cnt = len(func.__defaults__) if func.__defaults__ else 0

    def curried(first, *args):
        if args_cnt <= len(args) + default_args_cnt + 1:
            if iterable(args[len(args) - 1]):
                return func(first, *args)
        return functools.partial(func, first, *args)

    return curried


@curry
def t_filter(func, iterator):
    """일반적인 filter와 비슷"""

    for val in iterator:
        if func(val):
            yield val


@curry
def t_map(func, iterator):
    """일반적인 map과 비슷"""

    for val in iterator:
        yield func(val)


@curry
def reject(func, iterator):
    """filter 함수와 반대 결과인 경우 값 반환"""

    for val in iterator:
        if not func(val):
            yield val


@curry
def take(length, iterator):
    """입력값 length 번만 순회하여 값 반환"""

    for val in iterator:
        yield val
        length -= 1
        if length == 0:
            break


@curry
def reduce(func, acc, iterator=None):
    """일반적인 reduce와 비슷"""

    if not iterator:
        iterator = iter(acc)
        acc = next(iterator)

    for val in iterator:
        acc = func(acc, val)
    return acc


@curry
def for_each(func, iterator):
    """일반적인 for_each와 비슷"""
    for val in iterator:
        func(val)


def go(*args):
    """functional 함수를 우아하게 사용할 수 있다.
    >>> go([1, 2, 3, 4],
            map(lambda v: v + 1),
            filter(lambda v: v // 2),
            sum)
    6
    """

    return reduce(lambda acc, func: func(acc), args)


@curry
def find(func, iterator):
    """it에 f가 참인 index와 값을 반환
    >>> find(lambda v: v//2, [10, 20, 30, 40])
    (0, 10)
    """

    idx = 0
    for val in iterator:
        if func(val):
            return (idx, val)
        idx += 1
    return None
