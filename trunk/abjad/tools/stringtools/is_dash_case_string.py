# -*- encoding: utf-8 -*-
import re


hyphen_delimited_lowercase_regex_body = '(([a-z,0-9]+[-]+)*[a-z,0-9]+)?'
hyphen_delimited_lowercase_regex = re.compile('^%s$' % hyphen_delimited_lowercase_regex_body)

def is_dash_case_string(expr):
    r'''True when `expr` is a string and is hyphen delimited lowercase:

    ::

        >>> stringtools.is_dash_case_string('foo-bar')
        True

    False otherwise:

    ::

        >>> stringtools.is_dash_case_string('foo bar')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(hyphen_delimited_lowercase_regex.match(expr))
