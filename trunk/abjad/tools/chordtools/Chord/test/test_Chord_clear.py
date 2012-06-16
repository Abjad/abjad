from abjad import *


def test_Chord_clear_01():

    chord = Chord("<e' cs'' f''>4")
    chord.clear()

    assert len(chord) == 0
    assert chord.lilypond_format == '<>4'
