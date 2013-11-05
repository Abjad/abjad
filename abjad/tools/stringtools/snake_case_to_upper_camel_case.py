# -*- encoding: utf-8 -*-


def snake_case_to_upper_camel_case(string):
    '''Change underscore-delimited lowercase `string` to uppercamelcase:

    ::

        >>> string = 'bass_figure_alignment_positioning'
        >>> stringtools.snake_case_to_upper_camel_case(string)
        'BassFigureAlignmentPositioning'

    Returns string.
    '''

    parts = string.split('_')
    parts = [part.title() for part in parts]
    return ''.join(parts)
