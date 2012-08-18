import py.test
from abjad.tools import stringtools


def test_arg_to_bidirectional_direction_string_01():

    assert stringtools.arg_to_bidirectional_direction_string('^') == 'up'
    assert stringtools.arg_to_bidirectional_direction_string('_') == Down
    assert stringtools.arg_to_bidirectional_direction_string('up') == 'up'
    assert stringtools.arg_to_bidirectional_direction_string(Down) == Down
    assert stringtools.arg_to_bidirectional_direction_string(1) == 'up'
    assert stringtools.arg_to_bidirectional_direction_string(-1) == Down
    assert py.test.raises(ValueError,
        "stringtools.arg_to_bidirectional_direction_string('foo')")
