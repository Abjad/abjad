# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree___str___01():

    assert str(tonalanalysistools.ScaleDegree(1)) == '1'
    assert str(tonalanalysistools.ScaleDegree('flat', 2)) == 'b2'
    assert str(tonalanalysistools.ScaleDegree('sharp', 4)) == '#4'
