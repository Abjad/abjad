# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension_figured_bass_string_01():

    chord_suspension = tonalanalysistools.ChordSuspension(4, 3)
    assert chord_suspension.figured_bass_string == '4-3'

    chord_suspension = tonalanalysistools.ChordSuspension(('flat', 2), 1)
    assert chord_suspension.figured_bass_string == 'b2-1'

    chord_suspension = tonalanalysistools.ChordSuspension()
    assert chord_suspension.figured_bass_string == ''
