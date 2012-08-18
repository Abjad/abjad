import py.test
from abjad.tools import stringtools


def test_arg_to_bidirectional_lilypond_symbol_01():

    assert stringtools.arg_to_bidirectional_lilypond_symbol('^') == '^'
    assert stringtools.arg_to_bidirectional_lilypond_symbol('_') == '_'
    assert stringtools.arg_to_bidirectional_lilypond_symbol(Up) == '^'
    assert stringtools.arg_to_bidirectional_lilypond_symbol(Down) == '_'
    assert stringtools.arg_to_bidirectional_lilypond_symbol(1) == '^'
    assert stringtools.arg_to_bidirectional_lilypond_symbol(-1) == '_'
    assert py.test.raises(ValueError,
        "stringtools.arg_to_bidirectional_lilypond_symbol('foo')")
