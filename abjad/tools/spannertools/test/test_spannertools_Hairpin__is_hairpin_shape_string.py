# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin__is_hairpin_shape_string_01():

    assert Hairpin._is_hairpin_shape_string('<')
    assert Hairpin._is_hairpin_shape_string('>')


def test_spannertools_Hairpin__is_hairpin_shape_string_02():

    assert not Hairpin._is_hairpin_shape_string('@')
