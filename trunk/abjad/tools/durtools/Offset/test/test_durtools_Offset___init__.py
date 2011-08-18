from abjad.tools import durtools


def test_durtools_Offset___init___01():

    offset = durtools.Offset(121, 16)

    assert isinstance(offset, durtools.Offset)

