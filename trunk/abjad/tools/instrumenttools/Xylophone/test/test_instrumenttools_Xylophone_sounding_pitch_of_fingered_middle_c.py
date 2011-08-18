from abjad import *


def test_instrumenttools_Xylophone_sounding_pitch_of_fingered_middle_c_01():

    xylophone = instrumenttools.Xylophone()

    assert xylophone.sounding_pitch_of_fingered_middle_c == "c''"
