#-*- coding:utf-8 -*-

import sys
import functools
import inspect

if sys.version[0:3] == '2.7':
    from collections import Iterable
else:
    from collections.abc import Iterable

def is_number(v):
    try:
        int(v)
    except:
        return False
    else:
        return True

def iterable(obj):
    return isinstance(obj, Iterable)

def curry(f):
    args_cnt = len(inspect.getargspec(f).args)
    default_args_cnt = len(f.__defaults__) if f.__defaults__ else 0

    def curried(first, *args):
        if args_cnt <= len(args) + default_args_cnt + 1:
            if iterable(args[len(args) - 1]):
                return f(first, *args)
        return functools.partial(f, first, *args)

    return curried

@curry
def filter(f, it):
    for v in it:
        if f(v):
            yield v

@curry
def reject(f, it):
    for v in it:
        if not f(v):
            yield v

@curry
def map(f, it):
    for v in it:
        yield f(v)

@curry
def take(length, it):
    for v in it:
        yield v
        length -= 1
        if length == 0:
            break

@curry
def reduce(f, acc, it=None):
    if not it:
        it = iter(acc)
        acc = next(it)

    for v in it:
        acc = f(acc, v)
    return acc

@curry
def for_each(f, it):
    for v in it:
        f(v)

def go(*args):
    return reduce(lambda acc, f: f(acc), args)

@curry
def find(f, it):
    idx = 0
    for v in it:
        if f(v):
            return (idx, v)
        idx += 1