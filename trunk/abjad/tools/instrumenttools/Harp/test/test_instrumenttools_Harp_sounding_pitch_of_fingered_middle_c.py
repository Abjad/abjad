from abjad import *


def test_instrumenttools_Harp_sounding_pitch_of_fingered_middle_c_01():

    harp = instrumenttools.Harp()

    assert harp.sounding_pitch_of_fingered_middle_c == "c'"
