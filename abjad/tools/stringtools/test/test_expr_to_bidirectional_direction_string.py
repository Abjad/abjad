# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_expr_to_bidirectional_direction_string_01():

    assert stringtools.expr_to_bidirectional_direction_string('^') == 'up'
    assert stringtools.expr_to_bidirectional_direction_string('_') == 'down'
    assert stringtools.expr_to_bidirectional_direction_string(Up) == 'up'
    assert stringtools.expr_to_bidirectional_direction_string(Down) == 'down'
    assert stringtools.expr_to_bidirectional_direction_string(1) == 'up'
    assert stringtools.expr_to_bidirectional_direction_string(-1) == 'down'
    assert pytest.raises(ValueError,
        "stringtools.expr_to_bidirectional_direction_string('foo')")
