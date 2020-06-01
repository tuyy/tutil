# -*- coding:utf-8 -*-

"""
tutil.functional
~~~~~~~~~~~~~~~~

* is_number, iterable, curry
* filter, map, reduce, reject, find, take, for_each, go

copyright: (c) 2020 tuyy
license: MIT, see LICENSE for more details.
"""

import sys
import functools
import inspect


if sys.version[0:3] == '2.7':
    from collections import Iterable
    inspect.getfullargspec = inspect.getargspec
else:
    from collections.abc import Iterable


def is_number(v):
    """입력값 v 가 int형 변환이 가능하면 True, 아니면 False"""

    try:
        int(v)
    except TypeError:
        return False
    else:
        return True


def iterable(v):
    """입력값 v 가 iterable이면 True, 아니면 False"""

    return isinstance(v, Iterable)


def curry(f):
    """입력값 f를 curry하여 사용하기 위한 decorate 함수"""

    args_cnt = len(inspect.getfullargspec(f).args)
    default_args_cnt = len(f.__defaults__) if f.__defaults__ else 0

    def curried(first, *args):
        if args_cnt <= len(args) + default_args_cnt + 1:
            if iterable(args[len(args) - 1]):
                return f(first, *args)
        return functools.partial(f, first, *args)

    return curried


@curry
def filter(f, it):
    """일반적인 filter와 비슷"""

    for v in it:
        if f(v):
            yield v


@curry
def reject(f, it):
    """filter 함수와 반대 결과인 경우 값 반환"""

    for v in it:
        if not f(v):
            yield v


@curry
def map(f, it):
    """일반적인 map과 비슷"""

    for v in it:
        yield f(v)


@curry
def take(length, it):
    """입력값 length 번만 순회하여 값 반환"""

    for v in it:
        yield v
        length -= 1
        if length == 0:
            break


@curry
def reduce(f, acc, it=None):
    """일반적인 reduce와 비슷"""

    if not it:
        it = iter(acc)
        acc = next(it)

    for v in it:
        acc = f(acc, v)
    return acc


@curry
def for_each(f, it):
    """일반적인 for_each와 비슷"""
    for v in it:
        f(v)


def go(*args):
    """functional 함수를 우아하게 사용할 수 있다.
    go([1, 2, 3, 4],
        map(lambda v: v**v),
        filter(lambda v: v//2),
        reduce(lambda a, b: a + b))
    """

    return reduce(lambda acc, f: f(acc), args)


@curry
def find(f, it):
    """it에 f가 참인 index와 값을 반환
    >>> find(lambda v: v//2, [10, 20, 30, 40])
    (0, 10)
    """

    idx = 0
    for v in it:
        if f(v):
            return (idx, v)
        idx += 1
