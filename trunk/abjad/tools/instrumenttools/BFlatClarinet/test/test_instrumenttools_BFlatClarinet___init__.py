from abjad import *


def test_instrumenttools_BFlatClarinet___init___01():

    clarinet = instrumenttools.BFlatClarinet()

    assert isinstance(clarinet, instrumenttools.BFlatClarinet)
