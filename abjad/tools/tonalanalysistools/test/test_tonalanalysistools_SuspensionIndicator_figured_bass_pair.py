# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_SuspensionIndicator_figured_bass_pair_01():

    #assert tonalanalysistools.SuspensionIndicator(9, 8).figured_bass_pair == (9, 8)
    assert tonalanalysistools.SuspensionIndicator(7, 6).figured_bass_pair == (7, 6)
    assert tonalanalysistools.SuspensionIndicator(4, 3).figured_bass_pair == (4, 3)
    assert tonalanalysistools.SuspensionIndicator(2, 1).figured_bass_pair == (2, 1)
