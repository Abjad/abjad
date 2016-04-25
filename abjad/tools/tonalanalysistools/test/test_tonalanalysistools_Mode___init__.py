# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_Mode___init___01():
    r'''Initialize with mode name.
    '''

    mode = tonalanalysistools.Mode('dorian')
    assert mode.mode_name == 'dorian'


def test_tonalanalysistools_Mode___init___02():
    r'''Initialize with other mode instance.
    '''

    mode = tonalanalysistools.Mode('dorian')
    new = tonalanalysistools.Mode(mode)

    assert new.mode_name == 'dorian'
