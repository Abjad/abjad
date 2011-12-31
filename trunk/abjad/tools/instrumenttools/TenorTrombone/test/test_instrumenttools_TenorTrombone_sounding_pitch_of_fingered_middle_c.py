from abjad import *


def test_instrumenttools_TenorTrombone_sounding_pitch_of_fingered_middle_c_01():

    trombone = instrumenttools.TenorTrombone()

    assert trombone.sounding_pitch_of_fingered_middle_c == "c'"
