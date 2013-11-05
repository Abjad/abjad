# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_transpose_from_written_pitch_to_sounding_pitch_01():

    staff = Staff("<c' e' g'>4 d'4 r4 e'4")
    clarinet = instrumenttools.BFlatClarinet()
    attach(clarinet, staff)
    clarinet.instrument_name_markup = 'Clarinet in B-flat'
    clarinet.short_instrument_name_markup = 'Cl. B-flat'

    for leaf in staff.select_leaves():
        leaf.written_pitch_indication_is_at_sounding_pitch = False

    instrumenttools.transpose_from_written_pitch_to_sounding_pitch(staff)

    for leaf in staff.select_leaves():
        if isinstance(leaf, (Note, Chord)):
            assert leaf.written_pitch_indication_is_at_sounding_pitch

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. B-flat }
            <bf d' f'>4
            c'4
            r4
            d'4
        }
        '''
        )
