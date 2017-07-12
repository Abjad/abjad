# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_TonalAnalysisAgent_analyze_passing_tones_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    selection = abjad.analyze(staff[:])

    result = [False, True, True, False]
    assert selection.analyze_passing_tones() == result
