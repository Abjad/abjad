# -*- coding: utf-8 -*-
import re
import six
from abjad.tools.stringtools.is_dash_case \
    import hyphen_delimited_lowercase_regex_body


hyphen_delimited_lowercase_file_name_regex_body = """
    {}
    (\.[a-z,0-9]+)?
    """.format(hyphen_delimited_lowercase_regex_body)

hyphen_delimited_lowercase_file_name_regex = re.compile(
    '^{}$'.format(hyphen_delimited_lowercase_file_name_regex_body),
    re.VERBOSE,
    )


def is_dash_case_file_name(expr):
    r'''Is true when `expr` is a string and is hyphen-delimited lowercase 
    file name with extension.

    ..  container:: example

        ::

            >>> stringtools.is_dash_case_file_name('foo-bar')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_dash_case_file_name('foo.bar.blah')
            False

    Returns true or false.
    '''
    if not isinstance(expr, six.string_types):
        return False
    if expr == '':
        return True
    return bool(hyphen_delimited_lowercase_file_name_regex.match(expr))
