from abjad import *


def test_instrumenttools_SopranoVoice_sounding_pitch_of_fingered_middle_c_01():

    voice = instrumenttools.SopranoVoice()

    assert voice.sounding_pitch_of_fingered_middle_c == "c'"
