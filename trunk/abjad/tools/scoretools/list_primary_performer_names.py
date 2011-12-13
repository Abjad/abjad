def list_primary_performer_names():
    r'''.. versionadded:: 2.5
    
    List performer names::

        abjad> for performer_name in scoretools.list_primary_performer_names():
        ...     performer_name
        ... 
        'accordionist'
        'bassist'
        'bassoonist'
        'cellist'
        'clarinetist'
        'flutist'
        'guitarist'
        'harpist'
        'hornist'
        'oboist'
        'pianist'
        'trombonist'
        'trumpeter'
        'tubist'
        'violinist'
        'violist'

    Return list.
    '''
    from abjad.tools import instrumenttools

    performer_names = set([])

    for instrument_class in instrumenttools.list_instruments():
        instrument = instrument_class()    
        if instrument.is_primary_instrument:
            performer_name = instrument.get_default_performer_name()
            performer_names.add(performer_name)
    
    return list(sorted(performer_names))
