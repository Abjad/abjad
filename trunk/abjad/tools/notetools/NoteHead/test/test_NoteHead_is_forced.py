from abjad import *


def test_NoteHead_is_forced_01():

    note_head = notetools.NoteHead(written_pitch="c'")
    assert note_head.is_forced == False
    note_head.is_forced = True
    assert note_head.is_forced == True
    note_head.is_forced = False
    assert note_head.is_forced == False
