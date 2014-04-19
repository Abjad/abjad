# -*- encoding: utf-8 -*-
import sys


def is_string(expr):
    r'''Is true when `expr` is a string.

    Compatible under both Python 2.7.x and 3.x.
    '''
    if sys.version_info[0] == 2:
        if isinstance(expr, basestring):
            return True
    else:
        if isinstance(expr, str):
            return True
    return False
