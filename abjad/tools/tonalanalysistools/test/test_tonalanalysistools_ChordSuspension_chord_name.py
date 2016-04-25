# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension_chord_name_01():

    chord_suspension = tonalanalysistools.ChordSuspension(4, 3)
    assert chord_suspension.chord_name == 'sus4'

    chord_suspension = tonalanalysistools.ChordSuspension(('flat', 2), 1)
    assert chord_suspension.chord_name == 'susb2'

    chord_suspension = tonalanalysistools.ChordSuspension()
    assert chord_suspension.chord_name == ''
