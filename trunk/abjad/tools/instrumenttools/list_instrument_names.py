def list_instrument_names():
    r'''.. versionadded:: 2.5

    List instrument names::

        >>> for instrument_name in instrumenttools.list_instrument_names():
        ...     instrument_name
        ... 
        'accordion'
        'alto flute'
        'alto saxophone'
        'alto trombone'
        'clarinet in B-flat'
        'baritone saxophone'
        'baritone voice'
        'bass clarinet'
        'bass flute'
        'bass saxophone'
        'bass trombone'
        'bass voice'
        'bassoon'
        'cello'
        'clarinet in A'
        'contrabass'
        'contrabass clarinet'
        'contrabass flute'
        'contrabass saxophone'
        'contrabassoon'
        'contralto voice'
        'clarinet in E-flat'
        'English horn'
        'flute'
        'horn'
        'glockenspiel'
        'guitar'
        'harp'
        'harpsichord'
        'marimba'
        'mezzo-soprano voice'
        'oboe'
        'piano'
        'piccolo'
        'sopranino saxophone'
        'soprano saxophone'
        'soprano voice'
        'tenor saxophone'
        'tenor trombone'
        'tenor voice'
        'trumpet'
        'tuba'
        'untuned percussion'
        'vibraphone'
        'viola'
        'violin'
        'xylophone'

    Return list.
    '''
    from abjad.tools import instrumenttools

    instrument_names = []

    for instrument_class in instrumenttools.list_instruments():
        instrument = instrument_class()
        instrument_names.append(instrument.instrument_name)
    
    return instrument_names
