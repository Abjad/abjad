from abjad import *
import copy


def test_NoteHead___deepcopy___01():

    note_head_1 = notetools.NoteHead("cs''")
    note_head_1.tweak.color = 'red'

    note_head_2 = copy.deepcopy(note_head_1)

    assert isinstance(note_head_1, notetools.NoteHead)
    assert isinstance(note_head_2, notetools.NoteHead)
    assert note_head_1 == note_head_2
    assert note_head_1 is not note_head_2
    assert note_head_1.tweak == note_head_2.tweak
    assert note_head_1.tweak is not note_head_2.tweak
