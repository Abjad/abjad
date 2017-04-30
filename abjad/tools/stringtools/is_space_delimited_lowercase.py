# -*- coding: utf-8 -*-
import re
import six


space_delimited_lowercase_regex = re.compile(
    '^(([a-z,0-9]+[ ]+)*[a-z,0-9]+)?$',
    re.VERBOSE,
    )


def is_space_delimited_lowercase(argument):
    r'''Is true when `argument` is a string and is space-delimited lowercase.

    ..  container:: example

        ::

            >>> stringtools.is_space_delimited_lowercase('foo bar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_space_delimited_lowercase('foo_bar')
            False

    Returns true or false.
    '''
    if not isinstance(argument, six.string_types):
        return False
    return bool(space_delimited_lowercase_regex.match(argument))
