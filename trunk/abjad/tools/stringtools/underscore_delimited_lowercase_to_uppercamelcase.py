def underscore_delimited_lowercase_to_uppercamelcase(string):
    '''.. versionadded:: 2.0

    Change underscore-delimited lowercase `string` to uppercamelcase::

        >>> string = 'bass_figure_alignment_positioning'
        >>> stringtools.underscore_delimited_lowercase_to_uppercamelcase(string)
        'BassFigureAlignmentPositioning'

    Return string.
    '''

    parts = string.split('_')
    parts = [part.title() for part in parts]
    return ''.join(parts)
