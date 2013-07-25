def list_performer_names():
    r'''.. versionadded:: 2.5

    List performer names:

    ::

        >>> for performer_name in scoretools.list_performer_names():
        ...     performer_name
        ...
        'accordionist'
        'baritone'
        'bass'
        'bassist'
        'bassoonist'
        'cellist'
        'clarinetist'
        'contralto'
        'flutist'
        'guitarist'
        'harpist'
        'harpsichordist'
        'hornist'
        'mezzo-soprano'
        'oboist'
        'percussionist'
        'pianist'
        'saxophonist'
        'soprano'
        'tenor'
        'trombonist'
        'trumpeter'
        'tubist'
        'vibraphonist'
        'violinist'
        'violist'
        'xylophonist'

    Return list.
    '''
    from abjad.tools import scoretools
    return scoretools.Performer.list_performer_names()
