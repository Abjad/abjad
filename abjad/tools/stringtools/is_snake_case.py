# -*- coding: utf-8 -*-
import re
import six


underscore_delimited_lowercase_regex_body = '(([a-z,0-9]+[_]+)*[a-z,0-9]+)?'
underscore_delimited_lowercase_regex = re.compile(
    '^{}$'.format(underscore_delimited_lowercase_regex_body),
    re.VERBOSE,
    )


def is_snake_case(argument):
    r'''Is true when `argument` is a string and is underscore delimited lowercase.

    ..  container:: example

        ::

            >>> stringtools.is_snake_case('foo_bar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_snake_case('foo bar')
            False

    Returns true or false.
    '''
    if not isinstance(argument, six.string_types):
        return False
    return bool(underscore_delimited_lowercase_regex.match(argument))
