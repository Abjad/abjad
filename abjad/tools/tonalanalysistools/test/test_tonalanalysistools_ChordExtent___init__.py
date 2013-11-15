# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordExtent___init___01():
    r'''Initialize from number.
    '''

    assert tonalanalysistools.ChordExtent(7).number == 7


def test_tonalanalysistools_ChordExtent___init___02():
    r'''Initialize by reference.
    '''

    extent_indicator = tonalanalysistools.ChordExtent(7)
    new = tonalanalysistools.ChordExtent(extent_indicator)

    assert new.number == 7
    assert new == extent_indicator
    assert new is not extent_indicator
