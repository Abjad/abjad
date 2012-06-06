from abjad.tools.stringtools.is_underscore_delimited_lowercase_string import underscore_delimited_lowercase_regex_body
import re


underscore_delimited_lowercase_package_regex_body = """
    (%s\.)*
    %s
    """ % (underscore_delimited_lowercase_regex_body, underscore_delimited_lowercase_regex_body)

underscore_delimited_lowercase_package_regex = re.compile('^%s$' %
    underscore_delimited_lowercase_package_regex_body, re.VERBOSE)

def is_underscore_delimited_lowercase_package_name(expr):
    r'''.. versionadded:: 2.5

    True when `expr` is a string and is underscore-delimited lowercase package name::

        >>> stringtools.is_underscore_delimited_lowercase_package_name('foo.bar.blah_package')
        True
    
    False otherwise::

        >>> stringtools.is_underscore_delimited_lowercase_package_name('foo.bar.BlahPackage')
        False

    Return boolean.

    .. versionchanged:: 2.9
        renamed ``iotools.is_underscore_delimited_lowercase_package_name()`` to
        ``stringtools.is_underscore_delimited_lowercase_package_name()``.
    '''

    if not isinstance(expr, str):
        return False

    return bool(underscore_delimited_lowercase_package_regex.match(expr)) 
