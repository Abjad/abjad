from abjad.tools.instrumenttools._Instrument import _Instrument


def list_instruments(klasses=None):
    r'''.. versionadded:: 2.5

    List instruments in ``instrumenttools`` module::

        abjad> for instrument in instrumenttools.list_instruments():
        ...     instrument
        ... 
        <class 'abjad.tools.instrumenttools.Accordion.Accordion.Accordion'>
        <class 'abjad.tools.instrumenttools.AltoFlute.AltoFlute.AltoFlute'>
        <class 'abjad.tools.instrumenttools.BassClarinet.BassClarinet.BassClarinet'>
        <class 'abjad.tools.instrumenttools.BassFlute.BassFlute.BassFlute'>
        <class 'abjad.tools.instrumenttools.Bassoon.Bassoon.Bassoon'>
        <class 'abjad.tools.instrumenttools.Cello.Cello.Cello'>
        <class 'abjad.tools.instrumenttools.Clarinet.Clarinet.Clarinet'>
        <class 'abjad.tools.instrumenttools.Contrabass.Contrabass.Contrabass'>
        <class 'abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute.ContrabassFlute'>
        <class 'abjad.tools.instrumenttools.Contrabassoon.Contrabassoon.Contrabassoon'>
        <class 'abjad.tools.instrumenttools.EFlatClarinet.EFlatClarinet.EFlatClarinet'>
        <class 'abjad.tools.instrumenttools.EnglishHorn.EnglishHorn.EnglishHorn'>
        <class 'abjad.tools.instrumenttools.Flute.Flute.Flute'>
        <class 'abjad.tools.instrumenttools.FrenchHorn.FrenchHorn.FrenchHorn'>
        <class 'abjad.tools.instrumenttools.Glockenspiel.Glockenspiel.Glockenspiel'>
        <class 'abjad.tools.instrumenttools.Guitar.Guitar.Guitar'>
        <class 'abjad.tools.instrumenttools.Harp.Harp.Harp'>
        <class 'abjad.tools.instrumenttools.Marimba.Marimba.Marimba'>
        <class 'abjad.tools.instrumenttools.Oboe.Oboe.Oboe'>
        <class 'abjad.tools.instrumenttools.Piano.Piano.Piano'>
        <class 'abjad.tools.instrumenttools.Piccolo.Piccolo.Piccolo'>
        <class 'abjad.tools.instrumenttools.Trombone.Trombone.Trombone'>
        <class 'abjad.tools.instrumenttools.Trumpet.Trumpet.Trumpet'>
        <class 'abjad.tools.instrumenttools.Tuba.Tuba.Tuba'>
        <class 'abjad.tools.instrumenttools.UntunedPercussion.UntunedPercussion.UntunedPercussion'>
        <class 'abjad.tools.instrumenttools.Vibraphone.Vibraphone.Vibraphone'>
        <class 'abjad.tools.instrumenttools.Viola.Viola.Viola'>
        <class 'abjad.tools.instrumenttools.Violin.Violin.Violin'>
        <class 'abjad.tools.instrumenttools.Xylophone.Xylophone.Xylophone'>

    Return list.
    '''
    from abjad.tools import instrumenttools

    if klasses is None:
        klasses = (_Instrument, )

    instruments = []
    for value in instrumenttools.__dict__.itervalues():
        try:
            if issubclass(value, klasses):
                instruments.append(value)
        except TypeError:
            pass
    instruments.sort(lambda x, y: cmp(x.__name__, y.__name__))

    return instruments
