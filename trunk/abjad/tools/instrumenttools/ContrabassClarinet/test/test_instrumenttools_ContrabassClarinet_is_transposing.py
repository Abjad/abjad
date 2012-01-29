from abjad import *


def test_instrumenttools_ContrabassClarinet_is_transposing_01():

    contrabass_clarinet = instrumenttools.ContrabassClarinet()

    assert contrabass_clarinet.is_transposing
