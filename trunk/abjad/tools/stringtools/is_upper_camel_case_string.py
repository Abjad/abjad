# -*- encoding: utf-8 -*-
import re


uppercamelcase_regex = re.compile('^([A-Z,0-9]+[a-z,0-9]*)*$')

def is_upper_camel_case_string(expr):
    r'''.. versionadded:: 2.5

    True when `expr` is a string and is uppercamelcase:

    ::

        >>> stringtools.is_upper_camel_case_string('FooBar')
        True

    False otherwise:

    ::

        >>> stringtools.is_upper_camel_case_string('fooBar')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(uppercamelcase_regex.match(expr))
