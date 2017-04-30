# -*- coding: utf-8 -*-
import six


def is_string(argument):
    r'''Is true when `argument` is a string.

    Compatible under both Python 2.7.x and 3.x.
    '''
    return isinstance(argument, six.string_types)
