# -*- coding: utf-8 -*-
import re
import six


hyphen_delimited_lowercase_regex_body = '(([a-z,0-9]+[-]+)*[a-z,0-9]+)?'
hyphen_delimited_lowercase_regex = re.compile(
    '^{}$'.format(hyphen_delimited_lowercase_regex_body),
    re.VERBOSE,
    )


def is_dash_case(argument):
    r'''Is true when `argument` is a string and is hyphen delimited lowercase.

    ..  container:: example

        ::

            >>> stringtools.is_dash_case('foo-bar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_dash_case('foo bar')
            False

    Returns true or false.
    '''
    if not isinstance(argument, six.string_types):
        return False
    return bool(hyphen_delimited_lowercase_regex.match(argument))
