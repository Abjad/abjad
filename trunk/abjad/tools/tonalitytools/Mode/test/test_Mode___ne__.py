from abjad import *
from abjad.tools import tonalitytools


def test_Mode___ne___01():

    mode_1 = tonalitytools.Mode('dorian')
    mode_2 = tonalitytools.Mode('dorian')
    mode_3 = tonalitytools.Mode('phrygian')

    assert not mode_1 != mode_1
    assert not mode_1 != mode_2
    assert      mode_1 != mode_3
    assert not mode_2 != mode_1
    assert not mode_2 != mode_2
    assert      mode_2 != mode_3
    assert      mode_3 != mode_1
    assert      mode_3 != mode_2
    assert not mode_3 != mode_3
