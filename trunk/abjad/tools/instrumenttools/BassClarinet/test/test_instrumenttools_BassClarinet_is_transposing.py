from abjad import *


def test_instrumenttools_BassClarinet_is_transposing_01():

    bass_clarinet = instrumenttools.BassClarinet()

    assert bass_clarinet.is_transposing
