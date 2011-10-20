import re


underscore_delimited_lowercase_regex_body = '(([a-z]+[_]+)*[a-z]+)?'
underscore_delimited_lowercase_regex = re.compile('^%s$' % underscore_delimited_lowercase_regex_body)

def is_underscore_delimited_lowercase_string(expr):
    r'''.. versionadded:: 2.5

    True when `expr` is a string and is underscore delimited lowercase::

        abjad> iotools.is_underscore_delimited_lowercase_string('foo_bar')
        True
    
    False otherwise::

        abjad> iotools.is_underscore_delimited_lowercase_string('foo bar')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(underscore_delimited_lowercase_regex.match(expr)) 
