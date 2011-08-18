from abjad import *


def test_instrumenttools_Guitar_sounding_pitch_of_fingered_middle_c_01():

    guitar = instrumenttools.Guitar()

    assert guitar.sounding_pitch_of_fingered_middle_c == 'c'
