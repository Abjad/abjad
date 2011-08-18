from abjad import *


def test_instrumenttools_Flute_is_transposing_01():

    flute = instrumenttools.Flute()

    assert not flute.is_transposing
