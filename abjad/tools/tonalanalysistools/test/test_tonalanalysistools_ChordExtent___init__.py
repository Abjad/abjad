# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_tonalanalysistools_ChordExtent___init___01():
    r'''Initialize from number.
    '''

    assert tonalanalysistools.ChordExtent(7).number == 7


def test_tonalanalysistools_ChordExtent___init___02():
    r'''Initialize by reference.
    '''

    chord_extent = tonalanalysistools.ChordExtent(7)
    new = tonalanalysistools.ChordExtent(chord_extent)

    assert new.number == 7
    assert new == chord_extent
    assert new is not chord_extent
