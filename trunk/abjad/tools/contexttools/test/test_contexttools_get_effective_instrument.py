from abjad import *


def test_contexttools_get_effective_instrument_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    contexttools.InstrumentMark('Flute', 'Fl.')(staff)

    r'''
    \new Staff {
        \set Staff.instrumentName = \markup { Flute }
        \set Staff.shortInstrumentName = \markup { Fl. }
        c'8
        d'8
        e'8
        f'8
    }
    '''

    flute = contexttools.InstrumentMark('Flute', 'Fl.')
    assert contexttools.get_effective_instrument(staff) == flute
    assert contexttools.get_effective_instrument(staff[0]) == flute
    assert contexttools.get_effective_instrument(staff[1]) == flute
    assert contexttools.get_effective_instrument(staff[2]) == flute
    assert contexttools.get_effective_instrument(staff[3]) == flute
