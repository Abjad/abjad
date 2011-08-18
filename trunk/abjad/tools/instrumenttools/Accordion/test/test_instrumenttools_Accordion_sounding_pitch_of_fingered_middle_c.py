from abjad import *


def test_instrumenttools_Accordion_sounding_pitch_of_fingered_middle_c_01():

    accordion = instrumenttools.Accordion()

    assert accordion.sounding_pitch_of_fingered_middle_c == "c'"
