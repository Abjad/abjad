from abjad import *


def test_instrumenttools_Contrabassoon_souding_pitch_of_fingered_middle_c_01():

    contrabassoon = instrumenttools.Contrabassoon()

    assert contrabassoon.sounding_pitch_of_fingered_middle_c == 'c'
