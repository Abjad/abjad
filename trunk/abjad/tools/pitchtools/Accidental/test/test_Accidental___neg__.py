from abjad import *


def test_Accidental___neg___01():

    assert -pitchtools.Accidental('sharp') == pitchtools.Accidental('flat')
    assert -pitchtools.Accidental('flat') == pitchtools.Accidental('sharp')
    assert -pitchtools.Accidental('natural') == pitchtools.Accidental('natural')
