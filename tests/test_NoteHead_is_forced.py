import abjad


def test_NoteHead_is_forced_01():

    note_head = abjad.NoteHead(written_pitch="c'")
    assert note_head.is_forced is None
    note_head.is_forced = True
    assert note_head.is_forced is True
    note_head.is_forced = False
    assert note_head.is_forced is False
