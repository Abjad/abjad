# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordExtent_name_01():

    assert tonalanalysistools.ChordExtent(5).name == 'triad'
    assert tonalanalysistools.ChordExtent(7).name == 'seventh'
    assert tonalanalysistools.ChordExtent(9).name == 'ninth'
