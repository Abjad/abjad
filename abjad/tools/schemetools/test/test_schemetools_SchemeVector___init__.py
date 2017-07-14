# -*- coding: utf-8 -*-
import abjad


def test_schemetools_SchemeVector___init___01():

    vector = abjad.SchemeVector([1, 2, 3, 4])
    assert str(vector) == "'(1 2 3 4)"
    assert format(vector) == "#'(1 2 3 4)"


def test_schemetools_SchemeVector___init___02():

    vector = abjad.SchemeVector([True, False, 1, 0])
    assert str(vector) == "'(#t #f 1 0)"
    assert format(vector) == "#'(#t #f 1 0)"
