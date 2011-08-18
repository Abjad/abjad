from abjad import *


def test_instrumenttools_Marimba_is_transposing_01():

    marimba = instrumenttools.Marimba()

    assert not marimba.is_transposing
