# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension__initialize_by_reference_01():

    chord_suspension = tonalanalysistools.ChordSuspension(4, 3)
    u = tonalanalysistools.ChordSuspension(chord_suspension)

    assert chord_suspension is not u
    assert chord_suspension == u
