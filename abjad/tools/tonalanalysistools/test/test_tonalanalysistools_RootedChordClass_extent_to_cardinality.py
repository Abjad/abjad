# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_tonalanalysistools_RootedChordClass_extent_to_cardinality_01():

    assert tonalanalysistools.RootedChordClass.extent_to_cardinality(5) == 3
    assert tonalanalysistools.RootedChordClass.extent_to_cardinality(7) == 4
    assert tonalanalysistools.RootedChordClass.extent_to_cardinality(9) == 5
    assert tonalanalysistools.RootedChordClass.extent_to_cardinality(11) == 6
    assert tonalanalysistools.RootedChordClass.extent_to_cardinality(13) == 7


def test_tonalanalysistools_RootedChordClass_extent_to_cardinality_02():

    string = 'tonalanalysistools.RootedChordClass.extent_to_cardinality(1)'
    assert pytest.raises(Exception, string)
