def snake_case_to_upper_camel_case(string):
    '''.. versionadded:: 2.0

    Change underscore-delimited lowercase `string` to uppercamelcase:

    ::

        >>> string = 'bass_figure_alignment_positioning'
        >>> stringtools.snake_case_to_upper_camel_case(string)
        'BassFigureAlignmentPositioning'

    Return string.
    '''

    parts = string.split('_')
    parts = [part.title() for part in parts]
    return ''.join(parts)
