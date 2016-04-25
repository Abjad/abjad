# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_RootedChordClass_root_string_01():

    assert tonalanalysistools.RootedChordClass('c', 'major', 'triad').root_string == 'C'
    assert tonalanalysistools.RootedChordClass('c', 'minor', 'triad').root_string == 'c'
    assert tonalanalysistools.RootedChordClass('cs', 'major', 'triad').root_string == 'C#'
    assert tonalanalysistools.RootedChordClass('cs', 'minor', 'triad').root_string == 'c#'
    assert tonalanalysistools.RootedChordClass('cf', 'major', 'triad').root_string == 'Cb'
    assert tonalanalysistools.RootedChordClass('cf', 'minor', 'triad').root_string == 'cb'
