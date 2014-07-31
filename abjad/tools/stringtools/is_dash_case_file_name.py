# -*- encoding: utf-8 -*-
import re
from abjad.tools.stringtools.is_dash_case \
	import hyphen_delimited_lowercase_regex_body


hyphen_delimited_lowercase_file_name_regex_body = """
    %s
    (\.[a-z,0-9]+)?
    """ % hyphen_delimited_lowercase_regex_body

hyphen_delimited_lowercase_file_name_regex = re.compile('^%s$' %
    hyphen_delimited_lowercase_file_name_regex_body, re.VERBOSE)

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

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    if expr == '':
        return True

    return bool(hyphen_delimited_lowercase_file_name_regex.match(expr))