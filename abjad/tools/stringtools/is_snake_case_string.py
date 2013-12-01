# -*- encoding: utf-8 -*-
import re


underscore_delimited_lowercase_regex_body = '(([a-z,0-9]+[_]+)*[a-z,0-9]+)?'
underscore_delimited_lowercase_regex = re.compile('^%s$' % underscore_delimited_lowercase_regex_body)

def is_snake_case_string(expr):
    r'''True when `expr` is a string and is underscore delimited lowercase:

    ::

        >>> stringtools.is_snake_case_string('foo_bar')
        True

    Otherwise false:

    ::

        >>> stringtools.is_snake_case_string('foo bar')
        False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(underscore_delimited_lowercase_regex.match(expr))
