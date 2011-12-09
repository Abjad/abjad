from abjad.tools.instrumenttools.list_instruments import list_instruments


def list_secondary_instruments():
    r'''.. versionadded:: 2.5

    List secondary instruments::

        abjad> for secondary_instrument in instrumenttools.list_secondary_instruments():
        ...     secondary_instrument
        ... 
        <class 'abjad.tools.instrumenttools.AltoFlute.AltoFlute.AltoFlute'>
        <class 'abjad.tools.instrumenttools.BassClarinet.BassClarinet.BassClarinet'>
        <class 'abjad.tools.instrumenttools.BassFlute.BassFlute.BassFlute'>
        <class 'abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute.ContrabassFlute'>
        <class 'abjad.tools.instrumenttools.Contrabassoon.Contrabassoon.Contrabassoon'>
        <class 'abjad.tools.instrumenttools.EFlatClarinet.EFlatClarinet.EFlatClarinet'>
        <class 'abjad.tools.instrumenttools.EnglishHorn.EnglishHorn.EnglishHorn'>
        <class 'abjad.tools.instrumenttools.Glockenspiel.Glockenspiel.Glockenspiel'>
        <class 'abjad.tools.instrumenttools.Marimba.Marimba.Marimba'>
        <class 'abjad.tools.instrumenttools.Piccolo.Piccolo.Piccolo'>
        <class 'abjad.tools.instrumenttools.UntunedPercussion.UntunedPercussion.UntunedPercussion'>
        <class 'abjad.tools.instrumenttools.Vibraphone.Vibraphone.Vibraphone'>
        <class 'abjad.tools.instrumenttools.Xylophone.Xylophone.Xylophone'>

    Return list
    '''

    secondary_instruments = []

    for instrument_class in list_instruments():
        instrument = instrument_class()
        if instrument.is_secondary_instrument:
            secondary_instruments.append(instrument_class)

    return secondary_instruments        
