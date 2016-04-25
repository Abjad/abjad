# -*- coding: utf-8 -*-
from abjad import *


def test_tonalanalysistools_TonalAnalysisAgent_analyze_passing_tones_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    selection = tonalanalysistools.select(staff[:])

    result = [False, True, True, False]
    assert selection.analyze_passing_tones() == result
