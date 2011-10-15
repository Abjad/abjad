import re


uppercamelcase_regex = re.compile('^([A-Z]+[a-z]*)*$')

def is_uppercamelcase_string(expr):
    r'''.. versionadded:: 2.5

    True when `expr` is a string and is uppercamelcase::

        abjad> iotools.is_uppercamelcase_string('FooBar')
        True
    
    False otherwise::

        abjad> iotools.is_uppercamelcase_string('fooBar')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    return bool(uppercamelcase_regex.match(expr)) 
