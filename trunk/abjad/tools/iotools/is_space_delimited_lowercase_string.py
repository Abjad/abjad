import re


space_delimited_lowercase_regex = re.compile('^(([a-z]+[ ]+)*[a-z]+)?$')

def is_space_delimited_lowercase_string(expr):
    r'''.. versionadded:: 2.5

    True when `expr` is a string and is space-delimited lowercase::

        abjad> iotools.is_space_delimited_lowercase_string('foo bar')
        True
    
    False otherwise::

        abjad> iotools.is_space_delimited_lowercase_string('foo_bar')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(space_delimited_lowercase_regex.match(expr)) 
