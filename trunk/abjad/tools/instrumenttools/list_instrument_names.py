from abjad.tools.instrumenttools.list_instruments import list_instruments


def list_instrument_names(klasses=None):
    r'''.. versionadded:: 2.5

    List instrument names::

        abjad> for instrument_name in instrumenttools.list_instrument_names():
        ...     instrument_name
        ... 
        'Accordion'
        'Alto Flute'
        'Bass Clarinet'
        'Bass Flute'
        'Bassoon'
        'Cello'
        'Clarinet'
        'Contrabass'
        'Contrabass Flute'
        'Contrabassoon'
        'Clarinet in E-flat'
        'English Horn'
        'Flute'
        'French Horn'
        'Glockenspiel'
        'Guitar'
        'Harp'
        'Marimba'
        'Oboe'
        'Piano'
        'Piccolo'
        'Trombone'
        'Trumpet'
        'Tuba'
        'Percussion'
        'Vibraphone'
        'Viola'
        'Violin'
        'Xylophone'

    Return list.
    '''

    instrument_names = []

    for instrument_class in list_instruments():
        instrument = instrument_class()
        instrument_names.append(instrument.instrument_name_markup.contents_string)
    
    return instrument_names
