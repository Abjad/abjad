# -*- encoding: utf-8 -*-
import re


space_delimited_lowercase_regex = re.compile(
    '^(([a-z,0-9]+[ ]+)*[a-z,0-9]+)?$')

def is_space_delimited_lowercase(expr):
    r'''Is true when `expr` is a string and is space-delimited lowercase.

    ..  container:: example

        ::

            >>> stringtools.is_space_delimited_lowercase('foo bar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_space_delimited_lowercase('foo_bar')
            False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(space_delimited_lowercase_regex.match(expr))