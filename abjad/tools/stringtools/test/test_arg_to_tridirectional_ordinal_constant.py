# -*- encoding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_arg_to_tridirectional_ordinal_constant_01():

    assert stringtools.arg_to_tridirectional_ordinal_constant('^') is Up
    assert stringtools.arg_to_tridirectional_ordinal_constant('-') is Center
    assert stringtools.arg_to_tridirectional_ordinal_constant('_') is Down
    assert stringtools.arg_to_tridirectional_ordinal_constant(Up) is Up
    assert stringtools.arg_to_tridirectional_ordinal_constant('default') is Center
    assert stringtools.arg_to_tridirectional_ordinal_constant('neutral') is Center
    assert stringtools.arg_to_tridirectional_ordinal_constant(Down) is Down
    assert stringtools.arg_to_tridirectional_ordinal_constant(1) is Up
    assert stringtools.arg_to_tridirectional_ordinal_constant(0) is Center
    assert stringtools.arg_to_tridirectional_ordinal_constant(-1) is Down
    assert stringtools.arg_to_tridirectional_ordinal_constant(None) is None
    assert pytest.raises(ValueError,
        "stringtools.arg_to_tridirectional_ordinal_constant('foo')")
