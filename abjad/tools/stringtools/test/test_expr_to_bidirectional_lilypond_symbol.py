# -*- coding: utf-8 -*-
import pytest
from abjad.tools import stringtools


def test_to_bidirectional_lilypond_symbol_01():

    assert stringtools.to_bidirectional_lilypond_symbol('^') == '^'
    assert stringtools.to_bidirectional_lilypond_symbol('_') == '_'
    assert stringtools.to_bidirectional_lilypond_symbol(Up) == '^'
    assert stringtools.to_bidirectional_lilypond_symbol(Down) == '_'
    assert stringtools.to_bidirectional_lilypond_symbol(1) == '^'
    assert stringtools.to_bidirectional_lilypond_symbol(-1) == '_'
    assert pytest.raises(ValueError,
        "stringtools.to_bidirectional_lilypond_symbol('foo')")
