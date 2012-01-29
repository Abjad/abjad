from abjad import *


def test_instrumenttools_BassSaxophone_sounding_pitch_of_fingered_middle_c_01():

    bass_saxophone = instrumenttools.BassSaxophone()

    assert bass_saxophone.sounding_pitch_of_fingered_middle_c == 'bf,,'
