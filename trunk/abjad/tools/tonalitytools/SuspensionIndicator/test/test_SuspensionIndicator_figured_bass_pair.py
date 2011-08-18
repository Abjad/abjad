from abjad import *
from abjad.tools import tonalitytools


def test_SuspensionIndicator_figured_bass_pair_01():

    #assert tonalitytools.SuspensionIndicator(9, 8).figured_bass_pair == (9, 8)
    assert tonalitytools.SuspensionIndicator(7, 6).figured_bass_pair == (7, 6)
    assert tonalitytools.SuspensionIndicator(4, 3).figured_bass_pair == (4, 3)
    assert tonalitytools.SuspensionIndicator(2, 1).figured_bass_pair == (2, 1)
