# -*- encoding: utf-8 -*-
from abjad.tools.stringtools.is_snake_case_string \
	import underscore_delimited_lowercase_regex_body
import re


underscore_delimited_lowercase_package_regex_body = """
    (%s\.)*
    %s
    """ % (underscore_delimited_lowercase_regex_body, underscore_delimited_lowercase_regex_body)

underscore_delimited_lowercase_package_regex = re.compile('^%s$' %
    underscore_delimited_lowercase_package_regex_body, re.VERBOSE)

def is_snake_case_package_name(expr):
    r'''True when `expr` is a string and is underscore-delimited lowercase package name:

    ::

        >>> stringtools.is_snake_case_package_name('foo.bar.blah_package')
        True

    False otherwise:

    ::

        >>> stringtools.is_snake_case_package_name('foo.bar.BlahPackage')
        False

    Returns boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(underscore_delimited_lowercase_package_regex.match(expr))
