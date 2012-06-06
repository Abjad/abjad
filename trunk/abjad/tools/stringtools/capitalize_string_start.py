def capitalize_string_start(string):
    r'''.. versionadded:: 2.5

    Capitalize `string`::

        >>> string = 'violin I'

    ::

        >>> stringtools.capitalize_string_start(string)
        'Violin I'

    Function differs from built-in ``string.capitalize()``.

    This function affects only ``string[0]`` and leaves noninitial characters as-is.

    Built-in ``string.capitalize()`` forces noninitial characters to lowercase.

        >>> string.capitalize()
        'Violin i'

    Return newly constructed string.

    .. versionchanged:: 2.9
        renamed ``iotools.capitalize_string_start()`` to
        ``stringtools.capitalize_string_start()``.
    '''

    if not isinstance(string, str):
        raise TypeError

    if not string:
        return string
    else:
        return string[0].upper() + string[1:]
