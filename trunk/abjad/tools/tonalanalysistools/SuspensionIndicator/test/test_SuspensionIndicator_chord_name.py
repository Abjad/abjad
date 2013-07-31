# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_SuspensionIndicator_chord_name_01():

    t = tonalanalysistools.SuspensionIndicator(4, 3)
    assert t.chord_name == 'sus4'

    t = tonalanalysistools.SuspensionIndicator(('flat', 2), 1)
    assert t.chord_name == 'susb2'

    t = tonalanalysistools.SuspensionIndicator()
    assert t.chord_name == ''
