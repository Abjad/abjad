from abjad import *


def test_Chord___ne___01():

    chord_1 = Chord([0, 4, 7], (1, 4))
    chord_2 = Chord([0, 4, 7], (1, 4))
    chord_3 = Chord([0, 4, 6], (1, 4))

    assert chord_1 != chord_2
    assert chord_1 != chord_3
    assert chord_2 != chord_3
