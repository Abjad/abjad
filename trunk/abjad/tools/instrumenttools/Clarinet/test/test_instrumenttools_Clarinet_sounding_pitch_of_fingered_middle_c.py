from abjad import *


def test_instrumenttools_Clarinet_sounding_pitch_of_fingered_middle_c_01( ):

    clarinet = instrumenttools.Clarinet( )

    assert clarinet.sounding_pitch_of_fingered_middle_c == 'bf'
