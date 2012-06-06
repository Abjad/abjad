import re


uppercamelcase_regex = re.compile('^([A-Z,0-9]+[a-z,0-9]*)*$')

def is_uppercamelcase_string(expr):
    r'''.. versionadded:: 2.5

    True when `expr` is a string and is uppercamelcase::

        >>> stringtools.is_uppercamelcase_string('FooBar')
        True
    
    False otherwise::

        >>> stringtools.is_uppercamelcase_string('fooBar')
        False

    Return boolean.

    .. versionchanged:: 2.9
        renamed ``iotools.is_uppercamelcase_string()`` to
        ``stringtools.is_uppercamelcase_string()``.
    '''

    if not isinstance(expr, str):
        return False

    return bool(uppercamelcase_regex.match(expr)) 
