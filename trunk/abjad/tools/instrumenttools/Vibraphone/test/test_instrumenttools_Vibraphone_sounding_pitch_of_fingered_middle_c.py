from abjad import *


def test_instrumenttools_Vibraphone_sounding_pitch_of_fingered_middle_c_01():

    vibraphone = instrumenttools.Vibraphone()

    assert vibraphone.sounding_pitch_of_fingered_middle_c == "c'"
