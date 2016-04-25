# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RootedChordClass_quality_pair_01():

    cc = tonalanalysistools.RootedChordClass('c', 'major', 'triad', 'root')
    assert cc.quality_pair == ('major', 'triad')

    cc = tonalanalysistools.RootedChordClass('c', 'minor', 'triad', 'root')
    assert cc.quality_pair == ('minor', 'triad')


def test_tonalanalysistools_RootedChordClass_quality_pair_02():

    cc = tonalanalysistools.RootedChordClass('c', 'dominant', 'seventh', 'root')
    assert cc.quality_pair == ('dominant', 'seventh')

    cc = tonalanalysistools.RootedChordClass('c', 'diminished', 'seventh', 'root')
    assert cc.quality_pair == ('diminished', 'seventh')
