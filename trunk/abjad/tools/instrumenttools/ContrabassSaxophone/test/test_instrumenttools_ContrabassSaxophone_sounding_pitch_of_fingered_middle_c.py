from abjad import *


def test_instrumenttools_ContrabassSaxophone_sounding_pitch_of_fingered_middle_c_01():

    contrabass_saxophone = instrumenttools.ContrabassSaxophone()

    assert contrabass_saxophone.sounding_pitch_of_fingered_middle_c == 'ef,,'
