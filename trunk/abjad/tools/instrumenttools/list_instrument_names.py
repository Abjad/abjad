from abjad.tools.instrumenttools.list_instruments import list_instruments


def list_instrument_names(klasses=None):
    r'''.. versionadded:: 2.5

    List instrument names::

        abjad> for instrument_name in instrumenttools.list_instrument_names():
        ...     instrument_name
        ... 
        'accordion'
        'alto flute'
        'bass clarinet'
        'bass flute'
        'bassoon'
        'cello'
        'clarinet'
        'contrabass'
        'contrabass flute'
        'contrabassoon'
        'clarinet in E-flat'
        'English horn'
        'flute'
        'French horn'
        'glockenspiel'
        'guitar'
        'harp'
        'marimba'
        'oboe'
        'piano'
        'piccolo'
        'trombone'
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
