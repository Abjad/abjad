from abjad import *
import py.test


def test_ChordClass_extent_to_extent_name_01():

    assert tonalitytools.ChordClass.extent_to_extent_name(5) == 'triad'
    assert tonalitytools.ChordClass.extent_to_extent_name(7) == 'seventh'
    assert tonalitytools.ChordClass.extent_to_extent_name(9) == 'ninth'
    assert tonalitytools.ChordClass.extent_to_extent_name(11) == 'eleventh'
    assert tonalitytools.ChordClass.extent_to_extent_name(13) == 'thirteenth'


def test_ChordClass_extent_to_extent_name_02():

    string = 'tonalitytools.ChordClass.extent_to_extent_name(1)'
    assert py.test.raises(Exception, string)
