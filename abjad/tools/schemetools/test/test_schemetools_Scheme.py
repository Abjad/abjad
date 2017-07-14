# -*- coding: utf-8 -*-
import abjad


def test_schemetools_Scheme_01():
    r'''Scheme can be initialized from any value.
    '''

    scheme = abjad.Scheme(True)
    scheme = abjad.Scheme(False)
    scheme = abjad.Scheme(None)
    scheme = abjad.Scheme('hello')
    scheme = abjad.Scheme('hello world')
    scheme = abjad.Scheme([abjad.Scheme('foo'), abjad.Scheme(3.14159)])
    scheme = abjad.Scheme(
        [abjad.SchemePair(('padding', 1)),
            abjad.SchemePair(('attach-dir', -1))]
        )


def test_schemetools_Scheme_02():
    r'''Scheme takes an optional `quoting` keyword, for prepending
    quote/unquote ticks.
    '''

    scheme = abjad.Scheme(['fus', 'ro', 'dah'], quoting = "',")
    assert str(scheme) == "',(fus ro dah)"


def test_schemetools_Scheme_03():
    r'''__str__ of abjad.Scheme returns the abjad.Scheme formatted value without the hash
    mark, while format(Scheme) returns the formatted value with the hash mark,
    allowing for nested abjad.Scheme expressions.
    '''

    scheme = abjad.Scheme(['fus', 'ro', 'dah'], quoting = "'")
    assert str(scheme) == "'(fus ro dah)"
    assert format(scheme) == "#'(fus ro dah)"


def test_schemetools_Scheme_04():
    r'''Scheme attempts to format Python values into abjad.Scheme equivalents.
    '''

    assert format(abjad.Scheme(True)) == '##t'
    assert format(abjad.Scheme(False)) == '##f'
    assert format(abjad.Scheme(None)) == '##f'
    assert format(abjad.Scheme('hello world')) == '#"hello world"'
    assert format(abjad.Scheme([1, 2, 3])) == '#(1 2 3)'
    assert format(abjad.Scheme([
        abjad.SchemePair(('padding', 1)),
        abjad.SchemePair(('attach-dir', -1)),
        ],
        quoting="'",
        )) == "#'((padding . 1) (attach-dir . -1))"
