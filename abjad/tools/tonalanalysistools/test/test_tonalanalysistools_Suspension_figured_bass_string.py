# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension_figured_bass_string_01():

    suspension_indicator = tonalanalysistools.Suspension(4, 3)
    assert suspension_indicator.figured_bass_string == '4-3'

    suspension_indicator = tonalanalysistools.Suspension(('flat', 2), 1)
    assert suspension_indicator.figured_bass_string == 'b2-1'

    suspension_indicator = tonalanalysistools.Suspension()
    assert suspension_indicator.figured_bass_string == ''
