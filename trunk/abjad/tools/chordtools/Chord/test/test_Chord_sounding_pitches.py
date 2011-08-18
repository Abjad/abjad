from abjad import *


def test_Chord_sounding_pitches_01():

    staff = Staff("<c''' e'''>4 <d''' fs'''>4")
    glockenspiel = instrumenttools.Glockenspiel()(staff)
    instrumenttools.transpose_notes_and_chords_in_expr_from_sounding_pitch_to_fingered_pitch(staff)

    r'''
    \new Staff {
        \set Staff.instrumentName = \markup { Glockenspiel }
        \set Staff.shortInstrumentName = \markup { Gkspl. }
        <c' e'>4
        <d' fs'>4
    }
    '''

    assert staff[0].sounding_pitches == (
        pitchtools.NamedChromaticPitch("c'''"), pitchtools.NamedChromaticPitch("e'''"))
