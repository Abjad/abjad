# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_to_tridirectional_ordinal_constant_01():

    assert stringtools.to_tridirectional_ordinal_constant('^') == Up
    assert stringtools.to_tridirectional_ordinal_constant('-') == Center
    assert stringtools.to_tridirectional_ordinal_constant('_') == Down
    assert stringtools.to_tridirectional_ordinal_constant(Up) == Up
    assert stringtools.to_tridirectional_ordinal_constant('default') == Center
    assert stringtools.to_tridirectional_ordinal_constant('neutral') == Center
    assert stringtools.to_tridirectional_ordinal_constant(Down) == Down
    assert stringtools.to_tridirectional_ordinal_constant(1) == Up
    assert stringtools.to_tridirectional_ordinal_constant(0) == Center
    assert stringtools.to_tridirectional_ordinal_constant(-1) == Down
    assert stringtools.to_tridirectional_ordinal_constant(None) is None
    assert pytest.raises(ValueError,
        "stringtools.to_tridirectional_ordinal_constant('foo')")
