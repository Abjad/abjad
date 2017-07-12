# -*- coding: utf-8 -*-
import abjad


def test_schemetools_Scheme_format_scheme_value_01():

    assert abjad.Scheme.format_scheme_value(1) == '1'
    assert abjad.Scheme.format_scheme_value(True) == '#t'
    assert abjad.Scheme.format_scheme_value(False) == '#f'
    assert abjad.Scheme.format_scheme_value('foo bar') == '"foo bar"'
    assert abjad.Scheme.format_scheme_value('baz') == 'baz'
    assert abjad.Scheme.format_scheme_value([1, 2, 3]) == '(1 2 3)'
