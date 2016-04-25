# -*- coding: utf-8 -*-
import six


def is_string(expr):
    r'''Is true when `expr` is a string.

    Compatible under both Python 2.7.x and 3.x.
    '''
    return isinstance(expr, six.string_types)
