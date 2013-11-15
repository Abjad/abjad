# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Suspension_chord_name_01():

    suspension_indicator = tonalanalysistools.Suspension(4, 3)
    assert suspension_indicator.chord_name == 'sus4'

    suspension_indicator = tonalanalysistools.Suspension(('flat', 2), 1)
    assert suspension_indicator.chord_name == 'susb2'

    suspension_indicator = tonalanalysistools.Suspension()
    assert suspension_indicator.chord_name == ''
