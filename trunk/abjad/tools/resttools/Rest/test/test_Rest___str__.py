from abjad import *


def test_Rest___str___01():

    rest = Rest((1, 4))

    assert str(rest) == 'r4'
