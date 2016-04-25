# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_tonalanalysistools_RootedChordClass_cardinality_to_extent_01():

    assert tonalanalysistools.RootedChordClass.cardinality_to_extent(3) == 5
    assert tonalanalysistools.RootedChordClass.cardinality_to_extent(4) == 7
    assert tonalanalysistools.RootedChordClass.cardinality_to_extent(5) == 9
    assert tonalanalysistools.RootedChordClass.cardinality_to_extent(6) == 11
    assert tonalanalysistools.RootedChordClass.cardinality_to_extent(7) == 13


def test_tonalanalysistools_RootedChordClass_cardinality_to_extent_02():

    string = 'tonalanalysistools.RootedChordClass.cardinality_to_extent(1)'
    assert pytest.raises(Exception, string)

    string = 'tonalanalysistools.RootedChordClass.cardinality_to_extent(10)'
    assert pytest.raises(Exception, string)
