# -*- encoding: utf-8 -*-
from abjad import *


def test_HairpinSpanner_is_hairpin_shape_string_01():

    assert HairpinSpanner.is_hairpin_shape_string('<')
    assert HairpinSpanner.is_hairpin_shape_string('>')


def test_HairpinSpanner_is_hairpin_shape_string_02():

    assert not HairpinSpanner.is_hairpin_shape_string('@')
