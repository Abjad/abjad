# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_expr_to_tridirectional_ordinal_constant_01():

    assert stringtools.expr_to_tridirectional_ordinal_constant('^') == Up
    assert stringtools.expr_to_tridirectional_ordinal_constant('-') == Center
    assert stringtools.expr_to_tridirectional_ordinal_constant('_') == Down
    assert stringtools.expr_to_tridirectional_ordinal_constant(Up) == Up
    assert stringtools.expr_to_tridirectional_ordinal_constant('default') == Center
    assert stringtools.expr_to_tridirectional_ordinal_constant('neutral') == Center
    assert stringtools.expr_to_tridirectional_ordinal_constant(Down) == Down
    assert stringtools.expr_to_tridirectional_ordinal_constant(1) == Up
    assert stringtools.expr_to_tridirectional_ordinal_constant(0) == Center
    assert stringtools.expr_to_tridirectional_ordinal_constant(-1) == Down
    assert stringtools.expr_to_tridirectional_ordinal_constant(None) is None
    assert pytest.raises(ValueError,
        "stringtools.expr_to_tridirectional_ordinal_constant('foo')")
