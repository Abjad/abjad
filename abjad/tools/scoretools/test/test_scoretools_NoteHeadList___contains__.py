import abjad


def test_scoretools_NoteHeadList___contains___01():

    chord = abjad.Chord("<ef' cs'' f''>4")

    assert 17 in chord.note_heads
    assert 17.0 in chord.note_heads
    assert abjad.NamedPitch(17) in chord.note_heads
    assert abjad.NamedPitch("f''") in chord.note_heads
    assert chord.note_heads[1] in chord.note_heads
    assert abjad.NoteHead("f''") in chord.note_heads


def test_scoretools_NoteHeadList___contains___02():

    chord = abjad.Chord("<ef' cs'' f''>4")

    assert not 18 in chord.note_heads
    assert not 18.0 in chord.note_heads
    assert not abjad.NamedPitch(18) in chord.note_heads
    assert not abjad.NamedPitch("fs''") in chord.note_heads
    assert not abjad.NoteHead(18) in chord.note_heads
    assert not abjad.NoteHead("fs''") in chord.note_heads
