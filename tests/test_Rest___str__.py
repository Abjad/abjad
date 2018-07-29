import abjad


def test_Rest___str___01():

    rest = abjad.Rest((1, 4))

    assert str(rest) == 'r4'
