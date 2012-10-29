from abjad import *


def test_SchemePair_lilypond_format_01():
    '''Right-hand side string forces quotes.
    '''

    scheme_pair = schemetools.SchemePair('font-name', 'Times')
    assert scheme_pair.lilypond_format == '#\'(font-name . "Times")'


def test_SchemePair_lilypond_format_02():
    '''Right-hand side nonstring does not force quotes.
    '''

    scheme_pair = schemetools.SchemePair('spacing', 4)
    assert scheme_pair.lilypond_format == "#'(spacing . 4)"
