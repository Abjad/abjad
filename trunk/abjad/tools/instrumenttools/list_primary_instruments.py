def list_primary_instruments():
    r'''.. versionadded:: 2.5

    List primary instruments:

    ::

        >>> for instrument in instrumenttools.list_primary_instruments():
        ...     instrument.__name__
        ...
        'Accordion'
        'AltoSaxophone'
        'BaritoneVoice'
        'Bassoon'
        'BassVoice'
        'BFlatClarinet'
        'Cello'
        'Contrabass'
        'ContraltoVoice'
        'Flute'
        'FrenchHorn'
        'Guitar'
        'Harp'
        'Harpsichord'
        'MezzoSopranoVoice'
        'Oboe'
        'Piano'
        'SopranoVoice'
        'TenorTrombone'
        'TenorVoice'
        'Trumpet'
        'Tuba'
        'Viola'
        'Violin'

    Return list
    '''
    from abjad.tools import instrumenttools

    primary_instruments = []

    for instrument_class in instrumenttools.list_instruments():
        instrument = instrument_class()
        if instrument.is_primary_instrument:
            primary_instruments.append(instrument_class)

    return primary_instruments
