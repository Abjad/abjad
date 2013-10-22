# -*- encoding: utf-8 -*-


def capitalize_string_start(string):
    r'''Capitalize `string`:

    ::

        >>> string = 'violin I'

    ::

        >>> stringtools.capitalize_string_start(string)
        'Violin I'

    Function differs from built-in ``string.capitalize()``.

    This function affects only ``string[0]`` and leaves noninitial characters as-is.

    Built-in ``string.capitalize()`` forces noninitial characters to lowercase.

        >>> string.capitalize()
        'Violin i'

    Returns newly constructed string.
    '''

    if not isinstance(string, str):
        raise TypeError(string)

    if not string:
        return string
    else:
        return string[0].upper() + string[1:]
