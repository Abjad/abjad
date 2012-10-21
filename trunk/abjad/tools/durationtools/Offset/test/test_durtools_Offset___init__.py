from abjad import *


def test_durtools_Offset___init___01():

    offset = Offset(121, 16)

    assert isinstance(offset, Offset)
