from abjad import *


def test_Accidental_name_string_01():

    assert pitchtools.Accidental('s').name_string == 'sharp'
    assert pitchtools.Accidental('f').name_string == 'flat'

