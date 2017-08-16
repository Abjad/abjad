import abjad


def test_scoretools_NoteHeadList___delitem___01():
    '''Deletes note-head.
    '''

    chord = abjad.Chord("<ef' cs'' f''>4")
    del(chord.note_heads[1])

    assert format(chord) == "<ef' f''>4"
