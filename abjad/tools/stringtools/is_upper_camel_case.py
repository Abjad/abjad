# -*- encoding: utf-8 -*-
import re


uppercamelcase_regex = re.compile('^([A-Z,0-9]+[a-z,0-9]*)*$')

def is_upper_camel_case(expr):
    r'''Is true when `expr` is a string and is uppercamelcase.

    ..  container:: example

        ::

            >>> stringtools.is_upper_camel_case('FooBar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_upper_camel_case('fooBar')
            False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(uppercamelcase_regex.match(expr))