# -*- encoding: utf-8 -*-
import re
from abjad.tools.stringtools.is_snake_case \
	import underscore_delimited_lowercase_regex_body


underscore_delimited_lowercase_file_name_with_extension_regex_body = """
    %s
    \.
    [a-z,0-9]+
    """ % underscore_delimited_lowercase_regex_body

underscore_delimited_lowercase_file_name_with_extension_regex = re.compile(
    '^%s$' % 
    underscore_delimited_lowercase_file_name_with_extension_regex_body, 
    re.VERBOSE
    )

def is_snake_case_file_name_with_extension(expr):
    r'''Is true when `expr` is a string and is underscore-delimited lowercase 
    file name with extension.

    ..  container:: example

        ::

            >>> stringtools.is_snake_case_file_name_with_extension('foo_bar.blah')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_snake_case_file_name_with_extension('foo.bar.blah')
            False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    if expr == '':
        return True

    return bool(underscore_delimited_lowercase_file_name_with_extension_regex.match(expr))