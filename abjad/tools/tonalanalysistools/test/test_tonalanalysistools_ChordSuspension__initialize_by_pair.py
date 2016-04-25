# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension__initialize_by_pair_01():

    chord_suspension = tonalanalysistools.ChordSuspension((4, 3))

    assert chord_suspension.start == tonalanalysistools.ScaleDegree(4)
    assert chord_suspension.stop == tonalanalysistools.ScaleDegree(3)
