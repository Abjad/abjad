def space_delimited_lowercase_to_uppercamelcase(string):
    '''.. versionadded:: 2.6

    Change space-delimited lowercase `string` to uppercamelcase::

        abjad> string = 'bass figure alignment positioning'
        abjad> iotools.space_delimited_lowercase_to_uppercamelcase(string)
        'BassFigureAlignmentPositioning'

    Return string.
    '''

    parts = string.split(' ')
    parts = [part.title() for part in parts]
    return ''.join(parts)
