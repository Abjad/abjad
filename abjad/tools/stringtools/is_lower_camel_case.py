# -*- encoding: utf-8 -*-
import re


lowercamelcase_regex = re.compile('^([a-z,0-9]+([A-Z,0-9]+[a-z,0-9]*)*)?$')

def is_lower_camel_case(expr):
    r'''Is true when `expr` is a string and is lowercamelcase.

    ..  container:: example

        ::

            >>> stringtools.is_lower_camel_case('fooBar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_lower_camel_case('FooBar')
            False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(lowercamelcase_regex.match(expr))