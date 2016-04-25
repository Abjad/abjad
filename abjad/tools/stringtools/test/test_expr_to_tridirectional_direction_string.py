# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_expr_to_tridirectional_direction_string_01():

    assert stringtools.expr_to_tridirectional_direction_string('^') == 'up'
    assert stringtools.expr_to_tridirectional_direction_string('-') == 'center'
    assert stringtools.expr_to_tridirectional_direction_string('_') == 'down'
    assert stringtools.expr_to_tridirectional_direction_string(Up) == 'up'
    assert stringtools.expr_to_tridirectional_direction_string('default') == 'center'
    assert stringtools.expr_to_tridirectional_direction_string('neutral') == 'center'
    assert stringtools.expr_to_tridirectional_direction_string(Down) == 'down'
    assert stringtools.expr_to_tridirectional_direction_string(1) == 'up'
    assert stringtools.expr_to_tridirectional_direction_string(0) == 'center'
    assert stringtools.expr_to_tridirectional_direction_string(-1) == 'down'
    assert stringtools.expr_to_tridirectional_direction_string(None) == None
    assert pytest.raises(ValueError,
        "stringtools.expr_to_tridirectional_direction_string('foo')")
