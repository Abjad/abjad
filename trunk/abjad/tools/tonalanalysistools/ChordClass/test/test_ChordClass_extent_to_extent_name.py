from abjad import *
import py.test


def test_ChordClass_extent_to_extent_name_01():

    assert tonalanalysistools.ChordClass.extent_to_extent_name(5) == 'triad'
    assert tonalanalysistools.ChordClass.extent_to_extent_name(7) == 'seventh'
    assert tonalanalysistools.ChordClass.extent_to_extent_name(9) == 'ninth'
    assert tonalanalysistools.ChordClass.extent_to_extent_name(11) == 'eleventh'
    assert tonalanalysistools.ChordClass.extent_to_extent_name(13) == 'thirteenth'


def test_ChordClass_extent_to_extent_name_02():

    string = 'tonalanalysistools.ChordClass.extent_to_extent_name(1)'
    assert py.test.raises(Exception, string)
