# -*- encoding: utf-8 -*-
from abjad.tools.stringtools.is_snake_case_string \
	import underscore_delimited_lowercase_regex_body
import re


underscore_delimited_lowercase_file_name_regex_body = """
    %s
    (\.[a-z,0-9]+)?
    """ % underscore_delimited_lowercase_regex_body

underscore_delimited_lowercase_file_name_regex = re.compile('^%s$' %
    underscore_delimited_lowercase_file_name_regex_body, re.VERBOSE)

def is_snake_case_file_name(expr):
    r'''True when `expr` is a string and is underscore-delimited lowercase file name with extension:

    ::

        >>> stringtools.is_snake_case_file_name('foo_bar')
        True

    Otherwise false:

    ::

        >>> stringtools.is_snake_case_file_name('foo.bar.blah')
        False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    if expr == '':
        return True

    return bool(underscore_delimited_lowercase_file_name_regex.match(expr))
