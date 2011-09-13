from abjad import *


def test_Accidental___sub___01():

    m = pitchtools.Accidental('quarter sharp')

    assert m - m == pitchtools.Accidental('natural')
    assert m - m - m - m == pitchtools.Accidental('flat')
