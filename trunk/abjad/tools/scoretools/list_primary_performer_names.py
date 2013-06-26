def list_primary_performer_names():
    r'''.. versionadded:: 2.5

    List performer names::

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
    from abjad.tools import instrumenttools

    performer_names = set([])

    for instrument_class in instrumenttools.list_instruments():
        instrument = instrument_class()
        if instrument.is_primary_instrument:
            performer_name = instrument.get_default_performer_name()
            performer_abbreviation = getattr(
                instrument, 'default_performer_abbreviation', None)
            performer_abbreviation = performer_abbreviation or \
                instrument.default_short_instrument_name
            performer_names.add((performer_name, performer_abbreviation))

    return list(sorted(performer_names))
