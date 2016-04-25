# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree_name_01():

    assert tonalanalysistools.ScaleDegree(1).name == 'tonic'
    assert tonalanalysistools.ScaleDegree(2).name == 'superdominant'
    assert tonalanalysistools.ScaleDegree(3).name == 'mediant'
    assert tonalanalysistools.ScaleDegree(4).name == 'subdominant'
    assert tonalanalysistools.ScaleDegree(5).name == 'dominant'
    assert tonalanalysistools.ScaleDegree(6).name == 'submediant'
    assert tonalanalysistools.ScaleDegree(7).name == 'leading tone'
