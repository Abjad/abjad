from abjad import *


def test_HairpinSpanner_is_hairpin_shape_string_01():

    assert spannertools.HairpinSpanner.is_hairpin_shape_string('<')
    assert spannertools.HairpinSpanner.is_hairpin_shape_string('>')


def test_HairpinSpanner_is_hairpin_shape_string_02():

    assert not spannertools.HairpinSpanner.is_hairpin_shape_string('@')
