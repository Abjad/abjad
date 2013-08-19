# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_ChordClass___init___01():

    cc = tonalanalysistools.ChordClass('g', 'dominant', 7, 'root')
    assert repr(cc) == 'GDominantSeventhInRootPosition'
    assert len(cc) == 4
    assert cc.root == pitchtools.NamedPitchClass('g')
    assert cc.bass == pitchtools.NamedPitchClass('g')

    cc = tonalanalysistools.ChordClass('g', 'dominant', 7, 'first')
    assert repr(cc) == 'GDominantSeventhInFirstInversion'
    assert len(cc) == 4
    assert cc.root == pitchtools.NamedPitchClass('g')
    assert cc.bass == pitchtools.NamedPitchClass('b')
