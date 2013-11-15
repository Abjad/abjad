# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension_is_empty_01():

    suspension_indicator = tonalanalysistools.ChordSuspension()

    assert suspension_indicator.is_empty
