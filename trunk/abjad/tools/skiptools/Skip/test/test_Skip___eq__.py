from abjad import *


def test_Skip___eq___01():

    skip_1 = skiptools.Skip((1, 4))
    skip_2 = skiptools.Skip((1, 4))
    skip_3 = skiptools.Skip((1, 8))

    assert not skip_1 == skip_2
    assert not skip_1 == skip_3
    assert not skip_2 == skip_3
