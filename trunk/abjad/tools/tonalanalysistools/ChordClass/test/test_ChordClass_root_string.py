# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_ChordClass_root_string_01():

    assert tonalanalysistools.ChordClass('c', 'major', 'triad').root_string == 'C'
    assert tonalanalysistools.ChordClass('c', 'minor', 'triad').root_string == 'c'
    assert tonalanalysistools.ChordClass('cs', 'major', 'triad').root_string == 'C#'
    assert tonalanalysistools.ChordClass('cs', 'minor', 'triad').root_string == 'c#'
    assert tonalanalysistools.ChordClass('cf', 'major', 'triad').root_string == 'Cb'
    assert tonalanalysistools.ChordClass('cf', 'minor', 'triad').root_string == 'cb'
