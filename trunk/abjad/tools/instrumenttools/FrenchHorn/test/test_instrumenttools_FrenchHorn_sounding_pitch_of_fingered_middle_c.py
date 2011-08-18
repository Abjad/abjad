from abjad import *


def test_instrumenttools_FrenchHorn_sounding_pitch_of_fingered_middle_c_01():

    french_horn = instrumenttools.FrenchHorn()

    assert french_horn.sounding_pitch_of_fingered_middle_c == 'f'
