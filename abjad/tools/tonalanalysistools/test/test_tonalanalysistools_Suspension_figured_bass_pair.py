# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension_figured_bass_pair_01():

    #assert tonalanalysistools.Suspension(9, 8).figured_bass_pair == (9, 8)
    assert tonalanalysistools.Suspension(7, 6).figured_bass_pair == (7, 6)
    assert tonalanalysistools.Suspension(4, 3).figured_bass_pair == (4, 3)
    assert tonalanalysistools.Suspension(2, 1).figured_bass_pair == (2, 1)
