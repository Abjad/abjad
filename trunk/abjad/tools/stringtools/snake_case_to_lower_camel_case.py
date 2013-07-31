# -*- encoding: utf-8 -*-
def snake_case_to_lower_camel_case(string):
    '''.. versionadded:: 2.0

    Change underscore-delimited lowercase `string` to lowercamelcase:

    ::

        >>> string = 'bass_figure_alignment_positioning'
        >>> stringtools.snake_case_to_lower_camel_case(string)
        'bassFigureAlignmentPositioning'

    Return string.
    '''

    parts = string.split('_')
    first_part = parts[:1]
    rest_parts = parts[1:]
    rest_parts = [part.title() for part in rest_parts]
    all_parts = first_part + rest_parts
    return ''.join(all_parts)
