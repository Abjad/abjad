def underscore_delimited_lowercase_to_lowercamelcase(string):
    '''.. versionadded:: 2.0

    Change underscore-delimited lowercase `string` to lowercamelcase::

        >>> string = 'bass_figure_alignment_positioning'
        >>> stringtools.underscore_delimited_lowercase_to_lowercamelcase(string)
        'bassFigureAlignmentPositioning'

    .. versionchanged:: 2.0
        renamed ``stringtools.underscore_delimited_lowercase_to_lowercamelcase()`` to
        ``stringtools.underscore_delimited_lowercase_to_lowercamelcase()``.

    .. versionchanged:: 2.9
        renamed ``iotools.underscore_delimited_lowercase_to_lowercamelcase()`` to
        ``stringtools.underscore_delimited_lowercase_to_lowercamelcase()``.
    '''

    parts = string.split('_')
    first_part = parts[:1]
    rest_parts = parts[1:]
    rest_parts = [part.title() for part in rest_parts]
    all_parts = first_part + rest_parts
    return ''.join(all_parts)
