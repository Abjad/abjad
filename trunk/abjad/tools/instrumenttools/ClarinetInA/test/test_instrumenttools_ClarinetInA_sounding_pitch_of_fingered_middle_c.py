from abjad import *


def test_instrumenttools_ClarinetInA_sounding_pitch_of_fingered_middle_c_01():

    clarinet = instrumenttools.ClarinetInA()

    assert clarinet.sounding_pitch_of_fingered_middle_c == 'a'
