# -*- encoding: utf-8 -*-
import re


lowercamelcase_regex = re.compile('^([a-z,0-9]+([A-Z,0-9]+[a-z,0-9]*)*)?$')

def is_lower_camel_case_string(expr):
    r'''True when `expr` is a string and is lowercamelcase:

    ::

        >>> stringtools.is_lower_camel_case_string('fooBar')
        True

    Otherwise false:

    ::

        >>> stringtools.is_lower_camel_case_string('FooBar')
        False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(lowercamelcase_regex.match(expr))
