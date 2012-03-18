from abjad import *


def test_instrumenttools_ContraltoVoice_sounding_pitch_of_fingered_middle_c_01():

    voice = instrumenttools.ContraltoVoice()

    assert voice.sounding_pitch_of_fingered_middle_c == "c'"
