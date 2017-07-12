# -*- coding: utf-8 -*-
import abjad
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ScaleDegree__initialize_by_accidental_and_number_01():

    degree = tonalanalysistools.ScaleDegree('flat', 2)
    assert degree.accidental == abjad.Accidental('flat')
    assert degree.number == 2
