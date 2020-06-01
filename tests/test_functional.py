# -*- coding: utf-8 -*-


import pytest
import functools

from tutil.functional import *


def test_curry():
    def curry(f):
        def curried(first, *args):
            return lambda *args: f(first, *args)
        return curried

    def add(a, b, c):
        return a + b + c
    add5 = curry(add)(5)
    assert add5(5, 3) == 13


def test_curry2():
    @functools.partial
    def add(a, b, c):
        return a + b + c

    add15 = functools.partial(add, 5, 10)
    assert 25 == add15(10)

    first = reduce(lambda a, b: a + b)
    assert 6 == first(0, [1, 2, 3])

    second = reduce(lambda a, b: a + b, 0)
    assert 6 == second([1, 2, 3])

    third = reduce(lambda a, b: a + b)
    assert 6 == third([1, 2, 3])

    assert 6 == go([1, 2, 3, 4, 5],
                   map(lambda v: v),
                   take(3),
                   sum)


def test_old_and_new():
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    length = 3

    def calc_old(arr, length):
        rz = 0
        for v in arr:
            if v % 2:
                v = v*v
                rz += v
                length -= 1
                if length == 0:
                    break
        return rz

    def calc_new(arr, length):
        return reduce(lambda a, b: a + b, 0,
                      take(length,
                           map(lambda v: v * v,
                               filter(lambda v: v % 2, arr))))

    assert calc_old(arr, length) == calc_new(arr, length)


def test_foreach():
    arr = [1, 2, 3, 4, 5]
    rz, expected = [], []

    def for_old(arr):
        for v in arr:
            expected.append(v + 10)

    def for_new(arr):
        def f(v):
            rz.append(v)
        for_each(f, arr)

    assert for_old(arr) == for_new(arr)


def test_reduce_with_two_args():
    expected = reduce(lambda a, b: a + b, 0, [1, 2, 3, 4, 5])
    rz = reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])
    assert expected == rz


def test_map():
    rz = list(map(lambda v: v + 1, [1, 2, 3]))
    assert [2, 3, 4] == rz


def test_sum():
    rz = sum([1, 2, 3])
    assert 6 == rz


def test_reversed():
    rz = go(range(10),
            map(lambda v: v + 1),
            list,
            reversed,
            take(1),
            list)
    assert [10] == rz


def test_find():
    rz = go([1, 2, 3, 4, 5],
            find(lambda v: v == 3))
    assert (2, 3) == rz


def test_reject():
    rz = go([3, 4, 5],
            reject(lambda v: v//5),
            take(1),
            list)
    assert [3] == rz
