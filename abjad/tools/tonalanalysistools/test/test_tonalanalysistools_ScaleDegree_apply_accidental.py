# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree_apply_accidental_01():

    degree = tonalanalysistools.ScaleDegree('flat', 2)
    assert degree.apply_accidental('sharp') == tonalanalysistools.ScaleDegree(2)
    assert degree.apply_accidental('ss') == tonalanalysistools.ScaleDegree('sharp', 2)
