from abjad import *


def test_pitchtools_is_pitch_carrier_01():

    assert pitchtools.is_pitch_carrier(pitchtools.NamedChromaticPitch(0))
    assert pitchtools.is_pitch_carrier(Note("c'4"))
    assert pitchtools.is_pitch_carrier(notetools.NoteHead(None, 0))
    assert pitchtools.is_pitch_carrier(Chord([0, 2, 11], (1, 4)))


def test_pitchtools_is_pitch_carrier_02():

    assert not pitchtools.is_pitch_carrier(Staff([]))
    assert not pitchtools.is_pitch_carrier(Voice([]))
    assert not pitchtools.is_pitch_carrier(0)
    assert not pitchtools.is_pitch_carrier('foo')
