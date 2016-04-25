# -*- coding: utf-8 -*-
from abjad import *


def test_schemetools_Scheme_format_scheme_value_01():

    assert schemetools.Scheme.format_scheme_value(1) == '1'
    assert schemetools.Scheme.format_scheme_value(True) == '#t'
    assert schemetools.Scheme.format_scheme_value(False) == '#f'
    assert schemetools.Scheme.format_scheme_value('foo bar') == '"foo bar"'
    assert schemetools.Scheme.format_scheme_value('baz') == 'baz'
    assert schemetools.Scheme.format_scheme_value([1, 2, 3]) == '(1 2 3)'
