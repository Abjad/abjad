from abjad import *


def test_instrumenttools_AltoFlute_sounding_pitch_of_fingered_middle_c_01():

    alto_flute = instrumenttools.AltoFlute()

    assert alto_flute.sounding_pitch_of_fingered_middle_c == 'g'
