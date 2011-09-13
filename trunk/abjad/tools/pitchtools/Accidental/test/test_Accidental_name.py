from abjad import *


def test_Accidental_name_01():

    assert pitchtools.Accidental('s').name == 'sharp'
    assert pitchtools.Accidental('f').name == 'flat'
