from abjad import *


def test_instrumenttools_Glockenspiel_is_transposing_01():

    glockenspiel = instrumenttools.Glockenspiel()

    assert glockenspiel.is_transposing
