import abjad


def test_Container___contains___01():

    note = abjad.Note("c'4")
    voice = abjad.Voice([abjad.Note("c'4")])

    assert note not in voice
