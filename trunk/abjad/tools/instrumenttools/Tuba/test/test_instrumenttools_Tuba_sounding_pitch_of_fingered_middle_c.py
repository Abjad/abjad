from abjad import *


def test_instrumenttools_Tuba_sounding_pitch_of_fingered_middle_c_01():

    tuba = instrumenttools.Tuba()

    assert tuba.sounding_pitch_of_fingered_middle_c == "c'"
