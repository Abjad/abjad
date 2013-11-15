# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension_chord_name_01():

    suspension_indicator = tonalanalysistools.ChordSuspension(4, 3)
    assert suspension_indicator.chord_name == 'sus4'

    suspension_indicator = tonalanalysistools.ChordSuspension(('flat', 2), 1)
    assert suspension_indicator.chord_name == 'susb2'

    suspension_indicator = tonalanalysistools.ChordSuspension()
    assert suspension_indicator.chord_name == ''
