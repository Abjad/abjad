# -*- coding: utf-8 -*-
import six


def capitalize_start(string):
    r'''Capitalizes `string`.

    ..  container:: example

        ::

            >>> string = 'violin I'

    ..  container:: example

        ::

            >>> stringtools.capitalize_start(string)
            'Violin I'

    Function differs from built-in ``string.capitalize()``.

    This function affects only ``string[0]`` and leaves noninitial characters
    as-is.

    Built-in ``string.capitalize()`` forces noninitial characters to lowercase.

    ..  container:: example

        ::

            >>> string.capitalize()
            'Violin i'

    Returns newly constructed string.
    '''
    if not isinstance(string, six.string_types):
        raise ValueError(repr(string))
    if not string:
        return string
    else:
        return string[0].upper() + string[1:]