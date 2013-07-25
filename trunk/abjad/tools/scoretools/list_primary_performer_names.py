def list_primary_performer_names():
    r'''.. versionadded:: 2.5

    List performer names:

    ::

        >>> for pair in scoretools.list_primary_performer_names():
        ...     pair
        ...
        ('accordionist', 'acc.')
        ('baritone', 'bar.')
        ('bass', 'bass')
        ('bassist', 'vb.')
        ('bassoonist', 'bsn.')
        ('cellist', 'vc.')
        ('clarinetist', 'cl.')
        ('contralto', 'contr.')
        ('flutist', 'fl.')
        ('guitarist', 'gt.')
        ('harpist', 'hp.')
        ('harpsichordist', 'hpschd.')
        ('hornist', 'hn.')
        ('mezzo-soprano', 'ms.')
        ('oboist', 'ob.')
        ('pianist', 'pf.')
        ('saxophonist', 'alto sax.')
        ('soprano', 'sop.')
        ('tenor', 'ten.')
        ('trombonist', 'trb.')
        ('trumpeter', 'tp.')
        ('tubist', 'tb.')
        ('violinist', 'vn.')
        ('violist', 'va.')

    Return list.
    '''
    from abjad.tools import scoretools
    return scoretools.Performer.list_primary_performer_names()
