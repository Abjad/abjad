from abjad import *
from abjad.tools import tonalitytools


def test_ChordClass_root_string_01():

    assert tonalitytools.ChordClass('c', 'major', 'triad').root_string == 'C'
    assert tonalitytools.ChordClass('c', 'minor', 'triad').root_string == 'c'
    assert tonalitytools.ChordClass('cs', 'major', 'triad').root_string == 'C#'
    assert tonalitytools.ChordClass('cs', 'minor', 'triad').root_string == 'c#'
    assert tonalitytools.ChordClass('cf', 'major', 'triad').root_string == 'Cb'
    assert tonalitytools.ChordClass('cf', 'minor', 'triad').root_string == 'cb'
