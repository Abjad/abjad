from abjad import *


def test_instrumenttools_Piccolo_is_transposing_01():

    piccolo = instrumenttools.Piccolo()

    assert piccolo.is_transposing
