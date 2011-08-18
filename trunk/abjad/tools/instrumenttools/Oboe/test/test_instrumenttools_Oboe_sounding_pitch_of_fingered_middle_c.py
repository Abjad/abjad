from abjad import *


def test_instrumenttools_Oboe_sounding_pitch_of_fingered_middle_c_01():

    oboe = instrumenttools.Oboe()

    assert oboe.sounding_pitch_of_fingered_middle_c == "c'"
