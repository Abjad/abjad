from abjad import *
import py.test


def test_ChordClass_extent_to_cardinality_01():

    assert tonalitytools.ChordClass.extent_to_cardinality(5) == 3
    assert tonalitytools.ChordClass.extent_to_cardinality(7) == 4
    assert tonalitytools.ChordClass.extent_to_cardinality(9) == 5
    assert tonalitytools.ChordClass.extent_to_cardinality(11) == 6
    assert tonalitytools.ChordClass.extent_to_cardinality(13) == 7


def test_ChordClass_extent_to_cardinality_02():

    string = 'tonalitytools.ChordClass.extent_to_cardinality(1)'
    assert py.test.raises(Exception, string)
