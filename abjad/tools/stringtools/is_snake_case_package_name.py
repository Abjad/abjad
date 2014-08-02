# -*- encoding: utf-8 -*-
import re
from abjad.tools.stringtools.is_snake_case \
	import underscore_delimited_lowercase_regex_body


underscore_delimited_lowercase_package_regex_body = """
    (%s\.)*
    %s
    """ % (
        underscore_delimited_lowercase_regex_body, 
        underscore_delimited_lowercase_regex_body
        )

underscore_delimited_lowercase_package_regex = re.compile(
    '^%s$' %
    underscore_delimited_lowercase_package_regex_body, 
    re.VERBOSE
    )

def is_snake_case_package_name(expr):
    r'''Is true when `expr` is a string and is underscore-delimited lowercase 
    package name.

    ..  container:: example

        ::

            >>> stringtools.is_snake_case_package_name('foo.bar.blah_package')
            True

    Otherwise false:

    ..  container:: example

        ::

            >>> stringtools.is_snake_case_package_name('foo.bar.BlahPackage')
            False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(underscore_delimited_lowercase_package_regex.match(expr))