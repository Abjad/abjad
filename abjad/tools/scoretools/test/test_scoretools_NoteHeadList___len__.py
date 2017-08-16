import abjad


def test_scoretools_NoteHeadList___len___01():

    assert len(abjad.Chord('<>4').note_heads) == 0
    assert len(abjad.Chord("<ef'>4").note_heads) == 1
    assert len(abjad.Chord("<ef' cs''>4").note_heads) == 2
    assert len(abjad.Chord("<ef' cs'' f''>4").note_heads) == 3
