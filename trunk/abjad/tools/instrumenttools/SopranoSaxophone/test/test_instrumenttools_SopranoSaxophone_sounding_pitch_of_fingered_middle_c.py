from abjad import *


def test_instrumenttools_SopranoSaxophone_sounding_pitch_of_fingered_middle_c_01():

    soprano_saxophone = instrumenttools.SopranoSaxophone()

    assert soprano_saxophone.sounding_pitch_of_fingered_middle_c == 'bf'
