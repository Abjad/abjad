from abjad import *


def test_Skip__str___01():

    skip = skiptools.Skip((1, 4))

    assert str(skip) == 's4'
