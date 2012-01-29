from abjad.tools.instrumenttools.list_instruments import list_instruments


def list_primary_instruments():
    r'''.. versionadded:: 2.5

    List primary instruments::

        abjad> for primary_instrument in instrumenttools.list_primary_instruments():
        ...     primary_instrument
        ... 
        <class 'abjad.tools.instrumenttools.Accordion.Accordion.Accordion'>
        <class 'abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone.AltoSaxophone'>
        <class 'abjad.tools.instrumenttools.BFlatClarinet.BFlatClarinet.BFlatClarinet'>
        <class 'abjad.tools.instrumenttools.Bassoon.Bassoon.Bassoon'>
        <class 'abjad.tools.instrumenttools.Cello.Cello.Cello'>
        <class 'abjad.tools.instrumenttools.Contrabass.Contrabass.Contrabass'>
        <class 'abjad.tools.instrumenttools.Flute.Flute.Flute'>
        <class 'abjad.tools.instrumenttools.FrenchHorn.FrenchHorn.FrenchHorn'>
        <class 'abjad.tools.instrumenttools.Guitar.Guitar.Guitar'>
        <class 'abjad.tools.instrumenttools.Harp.Harp.Harp'>
        <class 'abjad.tools.instrumenttools.Harpsichord.Harpsichord.Harpsichord'>
        <class 'abjad.tools.instrumenttools.Oboe.Oboe.Oboe'>
        <class 'abjad.tools.instrumenttools.Piano.Piano.Piano'>
        <class 'abjad.tools.instrumenttools.TenorTrombone.TenorTrombone.TenorTrombone'>
        <class 'abjad.tools.instrumenttools.Trumpet.Trumpet.Trumpet'>
        <class 'abjad.tools.instrumenttools.Tuba.Tuba.Tuba'>
        <class 'abjad.tools.instrumenttools.Viola.Viola.Viola'>
        <class 'abjad.tools.instrumenttools.Violin.Violin.Violin'>

    Return list
    '''

    primary_instruments = []

    for instrument_class in list_instruments():
        instrument = instrument_class()
        if instrument.is_primary_instrument:
            primary_instruments.append(instrument_class)

    return primary_instruments        
