import abjad


def test_scoretools_NoteHead_tweaks_01():

    chord = abjad.Chord([0, 2, 10], (1, 4))

    chord.note_heads[0].tweaks.color = 'red'
    chord.note_heads[0].tweaks.thickness = 2

    chord.note_heads[1].tweaks.color = 'red'
    chord.note_heads[1].tweaks.thickness = 2

    chord.note_heads[2].tweaks.color = 'blue'

    tweaks_1 = chord.note_heads[0].tweaks
    tweaks_2 = chord.note_heads[1].tweaks
    tweaks_3 = chord.note_heads[2].tweaks

    assert tweaks_1 == tweaks_1
    assert tweaks_1 == tweaks_2
    assert tweaks_1 != tweaks_3
    assert tweaks_2 == tweaks_1
    assert tweaks_2 == tweaks_2
    assert tweaks_2 != tweaks_3
    assert tweaks_3 != tweaks_1
    assert tweaks_3 != tweaks_2
    assert tweaks_3 == tweaks_3
