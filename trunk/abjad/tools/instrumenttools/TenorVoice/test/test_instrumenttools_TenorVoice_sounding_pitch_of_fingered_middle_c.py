from abjad import *


def test_instrumenttools_TenorVoice_sounding_pitch_of_fingered_middle_c_01():

    voice = instrumenttools.TenorVoice()

    assert voice.sounding_pitch_of_fingered_middle_c == "c'"
