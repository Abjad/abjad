from abjad import *


def test_instrumenttools_BFlatClarinet_sounding_pitch_of_fingered_middle_c_01():

    clarinet = instrumenttools.BFlatClarinet()

    assert clarinet.sounding_pitch_of_fingered_middle_c == 'bf'
