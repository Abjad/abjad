from abjad import *


def test_instrumenttools_ContrabassClarinet_sounding_pitch_of_fingered_middle_c_01():

    contrabass_clarinet = instrumenttools.ContrabassClarinet()

    assert contrabass_clarinet.sounding_pitch_of_fingered_middle_c == 'bf,,'
