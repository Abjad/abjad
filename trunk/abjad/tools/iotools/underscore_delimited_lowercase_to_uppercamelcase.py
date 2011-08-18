def underscore_delimited_lowercase_to_uppercamelcase(string):
    '''.. versionadded:: 2.0

    Change underscore-delimited lowercase `string` to uppercamelcase::

        abjad> string = 'bass_figure_alignment_positioning'
        abjad> iotools.underscore_delimited_lowercase_to_uppercamelcase(string)
        'BassFigureAlignmentPositioning'

    .. versionchanged:: 2.0
        renamed ``stringtools.underscore_delimited_lowercase_to_uppercamelcase()`` to
        ``iotools.underscore_delimited_lowercase_to_uppercamelcase()``.
    '''

    parts = string.split('_')
    parts = [part.title() for part in parts]
    return ''.join(parts)
