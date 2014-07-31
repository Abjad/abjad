# -*- encoding: utf-8 -*-
import re


hyphen_delimited_lowercase_regex_body = '(([a-z,0-9]+[-]+)*[a-z,0-9]+)?'
hyphen_delimited_lowercase_regex = re.compile(
    '^%s$' % hyphen_delimited_lowercase_regex_body)

def is_dash_case(expr):
    r'''Is true when `expr` is a string and is hyphen delimited lowercase.

    ..  container:: example

        ::

            >>> stringtools.is_dash_case('foo-bar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_dash_case('foo bar')
            False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(hyphen_delimited_lowercase_regex.match(expr))