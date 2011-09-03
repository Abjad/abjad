from abjad import *


def test_Chord___len___01():

    assert len(Chord([], (1, 4))) == 0
    assert len(Chord([3], (1, 4))) == 1
    assert len(Chord([3, 13], (1, 4))) == 2
    assert len(Chord([3, 13, 17], (1, 4))) == 3
