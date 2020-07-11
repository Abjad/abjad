import abjad


def test_NoteHeadList___delitem___01():
    """
    Deletes note-head.
    """

    chord = abjad.Chord("<ef' cs'' f''>4")
    del chord.note_heads[1]

    assert abjad.lilypond(chord) == "<ef' f''>4"
