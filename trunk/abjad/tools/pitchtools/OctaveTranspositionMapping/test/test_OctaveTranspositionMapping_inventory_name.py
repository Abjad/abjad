from abjad import *


def test_OctaveTranspositionMapping_name_01():

    mapping = pitchtools.OctaveTranspositionMapping()
    assert mapping.name is None

    mapping.name = 'lower register mapping #2'
    assert mapping.name == 'lower register mapping #2'
