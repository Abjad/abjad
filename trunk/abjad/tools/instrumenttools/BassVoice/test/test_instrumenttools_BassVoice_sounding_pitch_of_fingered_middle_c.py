from abjad import *


def test_instrumenttools_BassVoice_sounding_pitch_of_fingered_middle_c_01():

    voice = instrumenttools.BassVoice()

    assert voice.sounding_pitch_of_fingered_middle_c == "c'"
