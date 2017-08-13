import abjad


def test_scoretools_Rest___cmp___01():

    rest_1 = abjad.Rest((1, 4))
    rest_2 = abjad.Rest((1, 4))
    rest_3 = abjad.Rest((1, 8))

    assert not rest_1 == rest_2
    assert not rest_1 == rest_3
    assert not rest_2 == rest_3


def test_scoretools_Rest___cmp___02():

    rest_1 = abjad.Rest((1, 4))
    rest_2 = abjad.Rest((1, 4))
    rest_3 = abjad.Rest((1, 8))

    assert rest_1 != rest_2
    assert rest_1 != rest_3
    assert rest_2 != rest_3
