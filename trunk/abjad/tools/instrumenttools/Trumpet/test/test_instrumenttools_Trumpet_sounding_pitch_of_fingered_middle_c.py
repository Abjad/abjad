from abjad import *


def test_instrumenttools_Trumpet_sounding_pitch_of_fingered_middle_c_01():

    trumpet = instrumenttools.Trumpet()

    assert trumpet.sounding_pitch_of_fingered_middle_c == "c'"
