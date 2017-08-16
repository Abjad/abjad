import abjad


def test_scoretools_Container___contains___01():

    note = abjad.Note("c'4")
    voice = abjad.Voice([abjad.Note("c'4")])

    assert not note in voice
