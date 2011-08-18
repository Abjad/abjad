def underscore_delimited_lowercase_to_lowercamelcase(string):
    '''.. versionadded:: 2.0

    Change underscore-delimited lowercase `string` to lowercamelcase::

        abjad> string = 'bass_figure_alignment_positioning'
        abjad> iotools.underscore_delimited_lowercase_to_lowercamelcase(string)
        'bassFigureAlignmentPositioning'

    .. versionchanged:: 2.0
        renamed ``stringtools.underscore_delimited_lowercase_to_lowercamelcase()`` to
        ``iotools.underscore_delimited_lowercase_to_lowercamelcase()``.
    '''

    parts = string.split('_')
    first_part = parts[:1]
    rest_parts = parts[1:]
    rest_parts = [part.title() for part in rest_parts]
    all_parts = first_part + rest_parts
    return ''.join(all_parts)
