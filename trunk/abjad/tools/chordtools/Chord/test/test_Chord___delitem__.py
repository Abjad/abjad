from abjad import *


def test_Chord___delitem___01():

    chord = Chord([3, 13, 17], (1, 4))
    del(chord[1])

    assert chord.format == "<ef' f''>4"
