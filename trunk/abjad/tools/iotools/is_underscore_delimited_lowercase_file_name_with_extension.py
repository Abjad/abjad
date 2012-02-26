from abjad.tools.iotools.is_underscore_delimited_lowercase_string import underscore_delimited_lowercase_regex_body
import re


underscore_delimited_lowercase_file_name_with_extension_regex_body = """
    %s
    \.
    [a-z,0-9]+
    """ % underscore_delimited_lowercase_regex_body

underscore_delimited_lowercase_file_name_with_extension_regex = re.compile('^%s$' %
    underscore_delimited_lowercase_file_name_with_extension_regex_body, re.VERBOSE)

def is_underscore_delimited_lowercase_file_name_with_extension(expr):
    r'''.. versionadded:: 2.7

    True when `expr` is a string and is underscore-delimited lowercase file name with extension::

        abjad> iotools.is_underscore_delimited_lowercase_file_name_with_extension('foo_bar.blah')
        True
    
    False otherwise::

        abjad> iotools.is_underscore_delimited_lowercase_file_name_with_extension('foo.bar.blah')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    if expr == '':
        return True

    return bool(underscore_delimited_lowercase_file_name_with_extension_regex.match(expr))
