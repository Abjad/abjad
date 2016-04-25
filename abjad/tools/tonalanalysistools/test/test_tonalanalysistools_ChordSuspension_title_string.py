# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordSuspension_title_string_01():

    chord_suspension = tonalanalysistools.ChordSuspension(4, 3)
    assert chord_suspension.title_string == 'FourThreeSuspension'

    chord_suspension = tonalanalysistools.ChordSuspension(('flat', 2), 1)
    assert chord_suspension.title_string == 'FlatTwoOneSuspension'

    chord_suspension = tonalanalysistools.ChordSuspension()
    assert chord_suspension.title_string == ''
