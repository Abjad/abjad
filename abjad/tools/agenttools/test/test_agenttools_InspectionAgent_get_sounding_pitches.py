# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_get_sounding_pitches_01():

    staff = Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = instrumenttools.Glockenspiel()
    attach(glockenspiel, staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Glockenspiel }
            \set Staff.shortInstrumentName = \markup { Gkspl. }
            <c' e'>4
            <d' fs'>4
        }
        '''
        )

    sounding_pitches = inspect_(staff[0]).get_sounding_pitches()
    assert sounding_pitches == (
        NamedPitch("c'''"),
        NamedPitch("e'''"),
        )
