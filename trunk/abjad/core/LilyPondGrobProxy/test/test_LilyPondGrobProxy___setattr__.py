from abjad import *


def test_LilyPondGrobProxy___setattr___01():

    note = Note("c'4")
    note.override.accidental.color = 'red'
    assert note.override.accidental.color == 'red'
