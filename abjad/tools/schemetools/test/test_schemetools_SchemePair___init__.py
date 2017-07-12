# -*- coding: utf-8 -*-
import abjad


def test_schemetools_SchemePair___init___01():
    r'''Initialize abjad.Scheme pair from two values.
    '''

    scheme_pair = abjad.SchemePair(1, 2)
    assert str(scheme_pair) == '(1 . 2)'

    scheme_pair = abjad.SchemePair(True, False)
    assert str(scheme_pair) == '(#t . #f)'

    scheme_pair = abjad.SchemePair('spacing', 4)
    assert str(scheme_pair) == '(spacing . 4)'


def test_schemetools_SchemePair___init___02():
    r'''Initialize abjad.Scheme pair from pair.
    '''

    scheme_pair = abjad.SchemePair((1, 2))
    assert str(scheme_pair) == '(1 . 2)'


def test_schemetools_SchemePair___init___03():
    r'''Initialize abjad.Scheme pair from other abjad.Scheme pair.
    '''

    scheme_pair_1 = abjad.SchemePair(1, 2)
    scheme_pair_2 = abjad.SchemePair(scheme_pair_1)

    assert str(scheme_pair_1) == '(1 . 2)'
    assert str(scheme_pair_2) == '(1 . 2)'
    assert scheme_pair_1 is not scheme_pair_2
