# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_ChordClass_cardinality_to_extent_01():

    assert tonalanalysistools.ChordClass.cardinality_to_extent(3) == 5
    assert tonalanalysistools.ChordClass.cardinality_to_extent(4) == 7
    assert tonalanalysistools.ChordClass.cardinality_to_extent(5) == 9
    assert tonalanalysistools.ChordClass.cardinality_to_extent(6) == 11
    assert tonalanalysistools.ChordClass.cardinality_to_extent(7) == 13


def test_ChordClass_cardinality_to_extent_02():

    string = 'tonalanalysistools.ChordClass.cardinality_to_extent(1)'
    assert py.test.raises(Exception, string)

    string = 'tonalanalysistools.ChordClass.cardinality_to_extent(10)'
    assert py.test.raises(Exception, string)
