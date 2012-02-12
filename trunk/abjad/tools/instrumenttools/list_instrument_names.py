from abjad.tools.instrumenttools.list_instruments import list_instruments


def list_instrument_names():
    r'''.. versionadded:: 2.5

    List instrument names::

        abjad> for instrument_name in instrumenttools.list_instrument_names():
        ...     instrument_name
        ... 
        'accordion'
        'alto flute'
        'alto saxophone'
        'alto trombone'
        'clarinet in B-flat'
        'baritone saxophone'
        'bass clarinet'
        'bass flute'
        'bass saxophone'
        'bass trombone'
        'bassoon'
        'cello'
        'clarinet in A'
        'contrabass'
        'contrabass clarinet'
        'contrabass flute'
        'contrabass saxophone'
        'contrabassoon'
        'clarinet in E-flat'
        'English horn'
        'flute'
        'horn'
        'glockenspiel'
        'guitar'
        'harp'
        'harpsichord'
        'marimba'
        'oboe'
        'piano'
        'piccolo'
        'sopranino saxophone'
        'soprano saxophone'
        'tenor saxophone'
        'tenor trombone'
        'trumpet'
        'tuba'
        'untuned percussion'
        'vibraphone'
        'viola'
        'violin'
        'xylophone'

    Return list.
    '''

    instrument_names = []

    for instrument_class in list_instruments():
        instrument = instrument_class()
        instrument_names.append(instrument.instrument_name)
    
    return instrument_names
