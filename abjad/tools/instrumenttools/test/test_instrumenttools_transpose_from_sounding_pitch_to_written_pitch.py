# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_transpose_from_sounding_pitch_to_written_pitch_01():

    staff = Staff("<c' e' g'>4 d'4 r4 e'4")
    clarinet = instrumenttools.BFlatClarinet()
    attach(clarinet, staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Clarinet in B-flat }
            \set Staff.shortInstrumentName = \markup { Cl. in B-flat }
            <d' fs' a'>4
            e'4
            r4
            fs'4
        }
        '''
        )
