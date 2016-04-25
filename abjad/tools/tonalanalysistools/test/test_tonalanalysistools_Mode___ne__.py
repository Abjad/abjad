# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Mode___ne___01():

    mode_1 = tonalanalysistools.Mode('dorian')
    mode_2 = tonalanalysistools.Mode('dorian')
    mode_3 = tonalanalysistools.Mode('phrygian')

    assert not mode_1 != mode_1
    assert not mode_1 != mode_2
    assert      mode_1 != mode_3
    assert not mode_2 != mode_1
    assert not mode_2 != mode_2
    assert      mode_2 != mode_3
    assert      mode_3 != mode_1
    assert      mode_3 != mode_2
    assert not mode_3 != mode_3
