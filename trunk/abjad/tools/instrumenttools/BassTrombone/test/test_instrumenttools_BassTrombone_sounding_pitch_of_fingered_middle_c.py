from abjad import *


def test_instrumenttools_BassTrombone_sounding_pitch_of_fingered_middle_c_01():

    trombone = instrumenttools.BassTrombone()

    assert trombone.sounding_pitch_of_fingered_middle_c == "c'"
