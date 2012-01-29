def list_performer_names(locale='en-us'):
    r'''.. versionadded:: 2.5
    
    List performer names::

        abjad> for performer_name in scoretools.list_performer_names():
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
        'harpsichordist'
        'hornist'
        'oboist'
        'percussionist'
        'pianist'
        'saxophonist'
        'trombonist'
        'trumpeter'
        'tubist'
        'vibraphonist'
        'violinist'
        'violist'
        'xylophonist'

    Available values for `locale` are ``'en-us'`` and ``'en-uk'``.
    '''
    from abjad.tools import instrumenttools

    performer_names = set([])

    for instrument_class in instrumenttools.list_instruments():
        instrument = instrument_class()    
        performer_name = instrument.get_default_performer_name(locale=locale)
        performer_names.add(performer_name)
    
    return list(sorted(performer_names))
