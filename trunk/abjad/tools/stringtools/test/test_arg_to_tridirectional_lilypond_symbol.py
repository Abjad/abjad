import py.test
from abjad.tools import stringtools


def test_arg_to_tridirectional_lilypond_symbol_01():

    assert stringtools.arg_to_tridirectional_lilypond_symbol('^') == '^'
    assert stringtools.arg_to_tridirectional_lilypond_symbol('-') == '-'
    assert stringtools.arg_to_tridirectional_lilypond_symbol('_') == '_'
    assert stringtools.arg_to_tridirectional_lilypond_symbol(Up) == '^'
    assert stringtools.arg_to_tridirectional_lilypond_symbol('default') == '-'
    assert stringtools.arg_to_tridirectional_lilypond_symbol('neutral') == '-'
    assert stringtools.arg_to_tridirectional_lilypond_symbol(Down) == '_'
    assert stringtools.arg_to_tridirectional_lilypond_symbol(1) == '^'
    assert stringtools.arg_to_tridirectional_lilypond_symbol(0) == '-'
    assert stringtools.arg_to_tridirectional_lilypond_symbol(-1) == '_'
    assert stringtools.arg_to_tridirectional_lilypond_symbol(None) == None
    assert py.test.raises(ValueError,
        "stringtools.arg_to_tridirectional_lilypond_symbol('foo')")
