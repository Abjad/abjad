import abjad


def test_scoretools_NoteHeadList___getitem___01():
    '''Gets note-head from chord.
    '''

    chord = abjad.Chord("<ef' cs'' f''>4")

    assert chord.note_heads[0] is chord.note_heads[0]
    assert chord.note_heads[1] is chord.note_heads[1]
    assert chord.note_heads[2] is chord.note_heads[2]
