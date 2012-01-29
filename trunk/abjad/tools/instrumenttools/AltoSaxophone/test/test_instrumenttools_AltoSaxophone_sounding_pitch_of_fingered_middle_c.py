from abjad import *


def test_instrumenttools_AltoSaxophone_sounding_pitch_of_fingered_middle_c_01():

    alto_saxophone = instrumenttools.AltoSaxophone()

    assert alto_saxophone.sounding_pitch_of_fingered_middle_c == 'ef'
