import py.test
from abjad.tools import stringtools


def test_arg_to_tridirectional_direction_string_01():

    assert stringtools.arg_to_tridirectional_direction_string('^') == Up
    assert stringtools.arg_to_tridirectional_direction_string('-') == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string('_') == Down
    assert stringtools.arg_to_tridirectional_direction_string(Up) == Up
    assert stringtools.arg_to_tridirectional_direction_string('default') == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string('neutral') == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string(Down) == Down
    assert stringtools.arg_to_tridirectional_direction_string(1) == Up
    assert stringtools.arg_to_tridirectional_direction_string(0) == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string(-1) == Down
    assert stringtools.arg_to_tridirectional_direction_string(None) == None
    assert py.test.raises(ValueError,
        "stringtools.arg_to_tridirectional_direction_string('foo')")
