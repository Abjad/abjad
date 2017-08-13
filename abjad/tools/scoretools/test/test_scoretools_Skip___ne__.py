import abjad


def test_scoretools_Skip___ne___01():

    skip_1 = abjad.Skip((1, 4))
    skip_2 = abjad.Skip((1, 4))
    skip_3 = abjad.Skip((1, 8))

    assert skip_1 != skip_2
    assert skip_1 != skip_3
    assert skip_2 != skip_3
