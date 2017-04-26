# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_to_tridirectional_direction_string_01():

    assert stringtools.to_tridirectional_direction_string('^') == 'up'
    assert stringtools.to_tridirectional_direction_string('-') == 'center'
    assert stringtools.to_tridirectional_direction_string('_') == 'down'
    assert stringtools.to_tridirectional_direction_string(Up) == 'up'
    assert stringtools.to_tridirectional_direction_string('default') == 'center'
    assert stringtools.to_tridirectional_direction_string('neutral') == 'center'
    assert stringtools.to_tridirectional_direction_string(Down) == 'down'
    assert stringtools.to_tridirectional_direction_string(1) == 'up'
    assert stringtools.to_tridirectional_direction_string(0) == 'center'
    assert stringtools.to_tridirectional_direction_string(-1) == 'down'
    assert stringtools.to_tridirectional_direction_string(None) == None
    assert pytest.raises(ValueError,
        "stringtools.to_tridirectional_direction_string('foo')")
