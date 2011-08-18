from abjad import *


def test_Chord___getitem___01():

    chord = Chord([3, 13, 17], (1, 4))

    assert chord[0] is chord.note_heads[0]
    assert chord[1] is chord.note_heads[1]
    assert chord[2] is chord.note_heads[2]
