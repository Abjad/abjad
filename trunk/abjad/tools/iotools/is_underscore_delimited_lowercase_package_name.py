from abjad.tools.iotools.is_underscore_delimited_lowercase_string import underscore_delimited_lowercase_regex_body
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

        abjad> iotools.is_underscore_delimited_lowercase_package_name('foo.bar.blah_package')
        True
    
    False otherwise::

        abjad> iotools.is_underscore_delimited_lowercase_package_name('foo.bar.BlahPackage')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(underscore_delimited_lowercase_package_regex.match(expr)) 
