# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_to_bidirectional_direction_string_01():

    assert stringtools.to_bidirectional_direction_string('^') == 'up'
    assert stringtools.to_bidirectional_direction_string('_') == 'down'
    assert stringtools.to_bidirectional_direction_string(Up) == 'up'
    assert stringtools.to_bidirectional_direction_string(Down) == 'down'
    assert stringtools.to_bidirectional_direction_string(1) == 'up'
    assert stringtools.to_bidirectional_direction_string(-1) == 'down'
    assert pytest.raises(ValueError,
        "stringtools.to_bidirectional_direction_string('foo')")
