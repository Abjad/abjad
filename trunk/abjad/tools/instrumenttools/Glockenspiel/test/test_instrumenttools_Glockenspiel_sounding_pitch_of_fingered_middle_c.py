from abjad import *


def test_instrumenttools_Glockenspiel_sounding_pitch_of_fingered_middle_c_01():

    glockenspiel = instrumenttools.Glockenspiel()

    assert glockenspiel.sounding_pitch_of_fingered_middle_c == "c'''"
