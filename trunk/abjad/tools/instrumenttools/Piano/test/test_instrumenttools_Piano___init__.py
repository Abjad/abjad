from abjad import *


def test_instrumenttools_Piano___init___01():

    piano = instrumenttools.Piano()

    assert isinstance(piano, instrumenttools.Piano)
