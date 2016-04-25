# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Mode___eq___01():

    mode_1 = tonalanalysistools.Mode('dorian')
    mode_2 = tonalanalysistools.Mode('dorian')
    mode_3 = tonalanalysistools.Mode('phrygian')

    assert      mode_1 == mode_1
    assert      mode_1 == mode_2
    assert not mode_1 == mode_3
    assert      mode_2 == mode_1
    assert      mode_2 == mode_2
    assert not mode_2 == mode_3
    assert not mode_3 == mode_1
    assert not mode_3 == mode_2
    assert      mode_3 == mode_3


def test_tonalanalysistools_Mode___eq___02():
    r'''Synonym modes do not compare equal, by definition.
    '''

    major = tonalanalysistools.Mode('major')
    ionian = tonalanalysistools.Mode('ionian')

    assert not major == ionian
    assert not ionian == major
