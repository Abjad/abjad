# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin_is_hairpin_shape_string_01():

    assert Hairpin.is_hairpin_shape_string('<')
    assert Hairpin.is_hairpin_shape_string('>')


def test_spannertools_Hairpin_is_hairpin_shape_string_02():

    assert not Hairpin.is_hairpin_shape_string('@')
