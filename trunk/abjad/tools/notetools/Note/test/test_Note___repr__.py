from abjad import *


def test_Note___repr___01():
    '''Note repr is evaluable.
    '''

    note_1 = Note("c'4")
    note_2 = eval(repr(note_1))

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert note_1.format == note_2.format
    assert note_1 is not note_2
