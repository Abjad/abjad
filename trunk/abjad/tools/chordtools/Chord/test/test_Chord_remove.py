from abjad import *


def test_Chord_remove_01():

    chord = Chord([3, 13, 17], (1, 4))
    note_head = chord[1]
    chord.remove(note_head)

    assert note_head._client is None
    assert chord.format == "<ef' f''>4"
