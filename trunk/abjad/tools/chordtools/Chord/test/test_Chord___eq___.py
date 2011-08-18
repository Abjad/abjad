from abjad import *


def test_Chord___eq____01():

    chord_1 = Chord([0, 4, 7], (1, 4))
    chord_2 = Chord([0, 4, 7], (1, 4))
    chord_3 = Chord([0, 4, 6], (1, 4))

    assert not chord_1 == chord_2
    assert not chord_1 == chord_3
    assert not chord_2 == chord_3
