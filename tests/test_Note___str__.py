import abjad


def test_Note___str___01():

    note = abjad.Note("c'4")

    assert str(note) == "c'4"
