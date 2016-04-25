# -*- coding: utf-8 -*-
from abjad import *


def test_schemetools_SchemePair_lilypond_format_01():
    r'''Right-hand side string forces quotes.
    '''

    scheme_pair = schemetools.SchemePair('font-name', 'Times')
    assert format(scheme_pair) == '#\'(font-name . "Times")'


def test_schemetools_SchemePair_lilypond_format_02():
    r'''Right-hand side nonstring does not force quotes.
    '''

    scheme_pair = schemetools.SchemePair('spacing', 4)
    assert format(scheme_pair) == "#'(spacing . 4)"
