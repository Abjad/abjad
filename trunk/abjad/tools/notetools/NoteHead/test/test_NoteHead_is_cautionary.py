from abjad import *


def test_NoteHead_is_cautionary_01():

    note_head = notetools.NoteHead(written_pitch="c'")
    assert note_head.is_cautionary == False
    note_head.is_cautionary = True
    assert note_head.is_cautionary == True
    note_head.is_cautionary = False
    assert note_head.is_cautionary == False
