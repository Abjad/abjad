def list_clef_names():
    r'''.. versionadded:: 2.8

    List clef names::

        >>> contexttools.list_clef_names()
        ['alto', 'baritone', 'bass', 'mezzosoprano', 'percussion', 'soprano', 'treble']

    Return list of strings.
    '''

    return list(sorted((
        'alto',
        'baritone',
        'bass',
        'mezzosoprano',
        'percussion',
        'soprano',
        'treble',
        )))
