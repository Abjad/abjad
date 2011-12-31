from abjad import *


def test_instrumenttools_AltoTrombone_sounding_pitch_of_fingered_middle_c_01():

    trombone = instrumenttools.AltoTrombone()

    assert trombone.sounding_pitch_of_fingered_middle_c == "c'"
