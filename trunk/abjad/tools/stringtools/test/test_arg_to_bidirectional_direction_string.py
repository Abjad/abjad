import py.test
from abjad.tools import stringtools


def test_arg_to_bidirectional_direction_string_01():

    assert stringtools.arg_to_bidirectional_direction_string('^') == 'up'
    assert stringtools.arg_to_bidirectional_direction_string('_') == 'down'
    assert stringtools.arg_to_bidirectional_direction_string(Up) == 'up'
    assert stringtools.arg_to_bidirectional_direction_string(Down) == 'down'
    assert stringtools.arg_to_bidirectional_direction_string(1) == 'up'
    assert stringtools.arg_to_bidirectional_direction_string(-1) == 'down'
    assert py.test.raises(ValueError,
        "stringtools.arg_to_bidirectional_direction_string('foo')")
