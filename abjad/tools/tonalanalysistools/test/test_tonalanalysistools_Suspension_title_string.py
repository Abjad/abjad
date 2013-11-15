# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension_title_string_01():

    suspension_indicator = tonalanalysistools.Suspension(4, 3)
    assert suspension_indicator.title_string == 'FourThreeSuspension'

    suspension_indicator = tonalanalysistools.Suspension(('flat', 2), 1)
    assert suspension_indicator.title_string == 'FlatTwoOneSuspension'

    suspension_indicator = tonalanalysistools.Suspension()
    assert suspension_indicator.title_string == ''
