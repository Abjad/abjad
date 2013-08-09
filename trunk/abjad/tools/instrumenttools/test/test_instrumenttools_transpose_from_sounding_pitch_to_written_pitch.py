# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_transpose_from_sounding_pitch_to_written_pitch_01():

    staff = Staff("<c' e' g'>4 d'4 r4 e'4")
    clarinet = instrumenttools.BFlatClarinet()(staff)
    clarinet.instrument_name_markup = 'Clarinet in B-flat'
    clarinet.short_instrument_name_markup = 'Cl. B-flat'

    for leaf in staff.select_leaves():
        if isinstance(leaf, (Note, Chord)):
            assert leaf.written_pitch_indication_is_at_sounding_pitch

    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    r'''
    \new Staff {
        \set Staff.instrumentName = \markup { Clarinet in B-flat }
        \set Staff.shortInstrumentName = \markup { Cl. B-flat }
        <d' fs' a'>4
        e'4
        r4
        fs'4
    }
    '''

    for leaf in staff.select_leaves():
        if isinstance(leaf, (Note, Chord)):
            assert not leaf.written_pitch_indication_is_at_sounding_pitch

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. B-flat }
            <d' fs' a'>4
            e'4
            r4
            fs'4
        }
        '''
        )
