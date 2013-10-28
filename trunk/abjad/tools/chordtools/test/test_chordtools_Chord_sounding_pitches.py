# -*- encoding: utf-8 -*-
from abjad import *


def test_chordtools_Chord_sounding_pitches_01():

    staff = Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = instrumenttools.Glockenspiel()
    attach(glockenspiel, staff)
    instrumenttools.transpose_from_sounding_pitch_to_written_pitch(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \set Staff.instrumentName = \markup { Glockenspiel }
            \set Staff.shortInstrumentName = \markup { Gkspl. }
            <c' e'>4
            <d' fs'>4
        }
        '''
        )

    assert staff[0].sounding_pitches == (
        pitchtools.NamedPitch("c'''"), 
        pitchtools.NamedPitch("e'''"),
        )
