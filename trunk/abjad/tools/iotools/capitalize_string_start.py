def capitalize_string_start(string):
    r'''.. versionadded:: 2.5

    Capitalize `string`::

        abjad> string = 'violin I'

    ::

        abjad> iotools.capitalize_string_start(string)
        'Violin I'

    Function differs from built-in ``string.capitalize()``.

    This function affects only ``string[0]`` and leaves noninitial characters as-is.

    Built-in ``string.capitalize()`` forces noninitial characters to lowercase.

        abjad> string.capitalize()
        'Violin i'

    Return newly constructed string.
    '''

    if not isinstance(string, str):
        raise TypeError

    if not string:
        return string
    else:
        return string[0].upper() + string[1:]
