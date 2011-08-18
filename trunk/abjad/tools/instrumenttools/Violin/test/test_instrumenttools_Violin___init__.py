from abjad import *


def test_instrumenttools_Violin___init___01():

    violin = instrumenttools.Violin()

    assert isinstance(violin, instrumenttools.Violin)
