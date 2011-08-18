from abjad import *


def test_instrumenttools_Bassoon_sounding_pitch_of_fingered_middle_c_01():

    bassoon = instrumenttools.Bassoon()

    assert bassoon.sounding_pitch_of_fingered_middle_c == "c'"
