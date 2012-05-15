import py.test
from abjad.tools import stringtools


def test_arg_to_tridirectional_direction_string_01():

    assert stringtools.arg_to_tridirectional_direction_string('^') == 'up'
    assert stringtools.arg_to_tridirectional_direction_string('-') == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string('_') == 'down'
    assert stringtools.arg_to_tridirectional_direction_string('up') == 'up'
    assert stringtools.arg_to_tridirectional_direction_string('default') == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string('neutral') == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string('down') == 'down'
    assert stringtools.arg_to_tridirectional_direction_string(1) == 'up'
    assert stringtools.arg_to_tridirectional_direction_string(0) == 'neutral'
    assert stringtools.arg_to_tridirectional_direction_string(-1) == 'down'
    assert stringtools.arg_to_tridirectional_direction_string(None) == None
    assert py.test.raises(ValueError,
        "stringtools.arg_to_tridirectional_direction_string('foo')")
