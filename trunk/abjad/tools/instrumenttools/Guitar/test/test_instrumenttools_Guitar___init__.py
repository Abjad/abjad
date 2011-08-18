from abjad import *


def test_instrumenttools_Guitar___init___01():

    guitar = instrumenttools.Guitar()

    assert isinstance(guitar, instrumenttools.Guitar)
