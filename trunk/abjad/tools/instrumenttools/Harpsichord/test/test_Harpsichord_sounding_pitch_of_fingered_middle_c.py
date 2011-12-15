from abjad import *


def test_Harpsichord_sounding_pitch_of_fingered_middle_c_01():

    harpsichord = instrumenttools.Harpsichord()

    assert harpsichord.sounding_pitch_of_fingered_middle_c == "c'"
