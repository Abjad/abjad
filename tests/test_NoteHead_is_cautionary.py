import abjad


def test_NoteHead_is_cautionary_01():

    note_head = abjad.NoteHead(written_pitch="c'")
    assert note_head.is_cautionary is None
    note_head.is_cautionary = True
    assert note_head.is_cautionary is True
    note_head.is_cautionary = False
    assert note_head.is_cautionary is False
