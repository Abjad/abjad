def list_instrument_names():
    r'''.. versionadded:: 2.5

    List instrument names:

    ::

        >>> for instrument_name in instrumenttools.list_instrument_names():
        ...     instrument_name
        ...
        'accordion'
        'alto flute'
        'alto saxophone'
        'alto trombone'
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
        'clarinet in B-flat'
        'clarinet in E-flat'
        'contrabass'
        'contrabass clarinet'
        'contrabass flute'
        'contrabass saxophone'
        'contrabassoon'
        'contralto voice'
        'English horn'
        'flute'
        'glockenspiel'
        'guitar'
        'harp'
        'harpsichord'
        'horn'
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

    instrument_names.sort(key=lambda x: x.lower())

    return instrument_names
