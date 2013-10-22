# -*- encoding: utf-8 -*-


def space_delimited_lowercase_to_upper_camel_case(string):
    '''Change space-delimited lowercase `string` to uppercamelcase:

    ::

        >>> string = 'bass figure alignment positioning'
        >>> stringtools.space_delimited_lowercase_to_upper_camel_case(string)
        'BassFigureAlignmentPositioning'

    Returns string.
    '''

    parts = string.split(' ')
    parts = [part.title() for part in parts]
    return ''.join(parts)
