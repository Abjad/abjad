from abjad.tools import durationtools


def test_durtools_Offset___init___01():

    offset = durationtools.Offset(121, 16)

    assert isinstance(offset, durationtools.Offset)
