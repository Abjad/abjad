# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_expr_to_tridirectional_lilypond_symbol_01():

    assert stringtools.expr_to_tridirectional_lilypond_symbol('^') == '^'
    assert stringtools.expr_to_tridirectional_lilypond_symbol('-') == '-'
    assert stringtools.expr_to_tridirectional_lilypond_symbol('_') == '_'
    assert stringtools.expr_to_tridirectional_lilypond_symbol(Up) == '^'
    assert stringtools.expr_to_tridirectional_lilypond_symbol('default') == '-'
    assert stringtools.expr_to_tridirectional_lilypond_symbol('neutral') == '-'
    assert stringtools.expr_to_tridirectional_lilypond_symbol(Down) == '_'
    assert stringtools.expr_to_tridirectional_lilypond_symbol(1) == '^'
    assert stringtools.expr_to_tridirectional_lilypond_symbol(0) == '-'
    assert stringtools.expr_to_tridirectional_lilypond_symbol(-1) == '_'
    assert stringtools.expr_to_tridirectional_lilypond_symbol(None) == None
    assert pytest.raises(ValueError,
        "stringtools.expr_to_tridirectional_lilypond_symbol('foo')")
