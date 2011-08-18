from abjad import *
from abjad.tools import tonalitytools


def test_ChordClass___init___01():

    cc = tonalitytools.ChordClass('g', 'dominant', 7, 'root')
    assert repr(cc) == 'GDominantSeventhInRootPosition'
    assert len(cc) == 4
    assert cc.root == pitchtools.NamedChromaticPitchClass('g')
    assert cc.bass == pitchtools.NamedChromaticPitchClass('g')

    cc = tonalitytools.ChordClass('g', 'dominant', 7, 'first')
    assert repr(cc) == 'GDominantSeventhInFirstInversion'
    assert len(cc) == 4
    assert cc.root == pitchtools.NamedChromaticPitchClass('g')
    assert cc.bass == pitchtools.NamedChromaticPitchClass('b')
