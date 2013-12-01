# -*- encoding: utf-8 -*-
import re


uppercamelcase_regex = re.compile('^([A-Z,0-9]+[a-z,0-9]*)*$')

def is_upper_camel_case_string(expr):
    r'''True when `expr` is a string and is uppercamelcase:

    ::

        >>> stringtools.is_upper_camel_case_string('FooBar')
        True

    Otherwise false:

    ::

        >>> stringtools.is_upper_camel_case_string('fooBar')
        False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(uppercamelcase_regex.match(expr))
