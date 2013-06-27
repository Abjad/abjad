def space_delimited_lowercase_to_upper_camel_case(string):
    '''.. versionadded:: 2.6

    Change space-delimited lowercase `string` to uppercamelcase:

    ::

        >>> string = 'bass figure alignment positioning'
        >>> stringtools.space_delimited_lowercase_to_upper_camel_case(string)
        'BassFigureAlignmentPositioning'

    Return string.
    '''

    parts = string.split(' ')
    parts = [part.title() for part in parts]
    return ''.join(parts)
