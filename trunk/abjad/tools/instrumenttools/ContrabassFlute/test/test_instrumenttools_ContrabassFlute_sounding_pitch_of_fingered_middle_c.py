from abjad import *


def test_instrumenttools_ContrabassFlute_sounding_pitch_of_fingered_middle_c_01():

    contrabass_flute = instrumenttools.ContrabassFlute()

    assert contrabass_flute.sounding_pitch_of_fingered_middle_c == 'g,'
