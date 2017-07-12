# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin__is_hairpin_shape_string_01():

    assert abjad.Hairpin._is_hairpin_shape_string('<')
    assert abjad.Hairpin._is_hairpin_shape_string('>')


def test_spannertools_Hairpin__is_hairpin_shape_string_02():

    assert not abjad.Hairpin._is_hairpin_shape_string('@')
