from abjad import *


def test_instrumenttools_Trombone_sounding_pitch_of_fingered_middle_c_01():

    trombone = instrumenttools.Trombone()

    assert trombone.sounding_pitch_of_fingered_middle_c == "c'"
