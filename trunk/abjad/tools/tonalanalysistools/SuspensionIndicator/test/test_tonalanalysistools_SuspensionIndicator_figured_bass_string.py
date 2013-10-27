# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_SuspensionIndicator_figured_bass_string_01():

    suspension_indicator = tonalanalysistools.SuspensionIndicator(4, 3)
    assert suspension_indicator.figured_bass_string == '4-3'

    suspension_indicator = tonalanalysistools.SuspensionIndicator(('flat', 2), 1)
    assert suspension_indicator.figured_bass_string == 'b2-1'

    suspension_indicator = tonalanalysistools.SuspensionIndicator()
    assert suspension_indicator.figured_bass_string == ''
