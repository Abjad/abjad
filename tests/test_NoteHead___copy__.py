import copy

import abjad


def test_NoteHead___copy___01():

    note_head_1 = abjad.NoteHead("cs''")
    note_head_1.is_cautionary = True
    note_head_1.is_forced = True
    abjad.tweak(note_head_1).color = "red"
    abjad.tweak(note_head_1).font_size = -2

    note_head_2 = copy.copy(note_head_1)

    assert isinstance(note_head_1, abjad.NoteHead)
    assert isinstance(note_head_2, abjad.NoteHead)
    assert note_head_1 == note_head_2
    assert note_head_1 is not note_head_2
    assert note_head_1.is_cautionary == note_head_2.is_cautionary
    assert note_head_1.is_forced == note_head_2.is_forced
    assert note_head_1.tweaks == note_head_2.tweaks
    assert note_head_1.tweaks is not note_head_2.tweaks
