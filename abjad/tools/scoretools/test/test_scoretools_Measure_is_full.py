import abjad


def test_scoretools_Measure_is_full_01():

    assert abjad.Measure((3, 8), "c'8 d'8 e'8").is_full
    assert not abjad.Measure((3, 8), "c'8 d'8").is_full
    assert not abjad.Measure((3, 8), "c'8 d'8 e'8 f'8").is_full
