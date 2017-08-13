import abjad


def test_scoretools_Chord___str___01():

    chord = abjad.Chord("<ef' cs'' f''>4")

    assert str(chord) == "<ef' cs'' f''>4"
