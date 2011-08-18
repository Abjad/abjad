from abjad import *


def test_instrumenttools_Violin_sounding_pitch_of_fingered_middle_c_01():

    violin = instrumenttools.Violin()

    assert violin.sounding_pitch_of_fingered_middle_c == "c'"
