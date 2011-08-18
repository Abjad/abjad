from abjad import *


def test_instrumenttools_Piccolo_sounding_pitch_of_fingered_middle_c_01():

    piccolo = instrumenttools.Piccolo()

    assert piccolo.sounding_pitch_of_fingered_middle_c == "c''"
