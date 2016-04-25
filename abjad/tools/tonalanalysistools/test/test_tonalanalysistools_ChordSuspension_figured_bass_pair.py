# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension_figured_bass_pair_01():

    #assert tonalanalysistools.ChordSuspension(9, 8).figured_bass_pair == (9, 8)
    assert tonalanalysistools.ChordSuspension(7, 6).figured_bass_pair == (7, 6)
    assert tonalanalysistools.ChordSuspension(4, 3).figured_bass_pair == (4, 3)
    assert tonalanalysistools.ChordSuspension(2, 1).figured_bass_pair == (2, 1)
