# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree_title_string_01():

    assert tonalanalysistools.ScaleDegree(1).title_string == 'One'
    assert tonalanalysistools.ScaleDegree(2).title_string == 'Two'
    assert tonalanalysistools.ScaleDegree(3).title_string == 'Three'
    assert tonalanalysistools.ScaleDegree(4).title_string == 'Four'
    assert tonalanalysistools.ScaleDegree(5).title_string == 'Five'
    assert tonalanalysistools.ScaleDegree(6).title_string == 'Six'
    assert tonalanalysistools.ScaleDegree(7).title_string == 'Seven'


def test_tonalanalysistools_ScaleDegree_title_string_02():

    assert tonalanalysistools.ScaleDegree('sharp', 4).title_string == 'SharpFour'
    assert tonalanalysistools.ScaleDegree('flat', 6).title_string == 'FlatSix'
