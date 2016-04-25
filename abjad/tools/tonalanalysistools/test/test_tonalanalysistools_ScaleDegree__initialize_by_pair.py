# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree__initialize_by_pair_01():

    degree = tonalanalysistools.ScaleDegree(('flat', 2))

    assert degree.accidental == pitchtools.Accidental('flat')
    assert degree.number == 2
