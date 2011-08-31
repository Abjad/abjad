from abjad import *
from abjad.tools import tonalitytools


def test_SuspensionIndicator_chord_name_01():

    t = tonalitytools.SuspensionIndicator(4, 3)
    assert t.chord_name == 'sus4'

    t = tonalitytools.SuspensionIndicator(('flat', 2), 1)
    assert t.chord_name == 'susb2'

    t = tonalitytools.SuspensionIndicator()
    assert t.chord_name == ''
