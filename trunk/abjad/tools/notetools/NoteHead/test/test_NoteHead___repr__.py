from abjad import *
from abjad.tools.notetools import NoteHead


def test_NoteHead___repr___01():
    '''Note head repr is evaluable.
    '''

    note_head_1 = notetools.NoteHead("cs''")
    note_head_2 = eval(repr(note_head_1))

    assert isinstance(note_head_1, notetools.NoteHead)
    assert isinstance(note_head_2, notetools.NoteHead)
    assert note_head_1 == note_head_2
    assert note_head_1 is not note_head_2
