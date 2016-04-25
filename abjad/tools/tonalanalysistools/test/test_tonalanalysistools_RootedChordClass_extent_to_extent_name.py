# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_tonalanalysistools_RootedChordClass_extent_to_extent_name_01():

    assert tonalanalysistools.RootedChordClass.extent_to_extent_name(5) == 'triad'
    assert tonalanalysistools.RootedChordClass.extent_to_extent_name(7) == 'seventh'
    assert tonalanalysistools.RootedChordClass.extent_to_extent_name(9) == 'ninth'
    assert tonalanalysistools.RootedChordClass.extent_to_extent_name(11) == 'eleventh'
    assert tonalanalysistools.RootedChordClass.extent_to_extent_name(13) == 'thirteenth'


def test_tonalanalysistools_RootedChordClass_extent_to_extent_name_02():

    string = 'tonalanalysistools.RootedChordClass.extent_to_extent_name(1)'
    assert pytest.raises(Exception, string)
