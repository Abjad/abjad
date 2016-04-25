# -*- coding: utf-8 -*-
from abjad.tools.schemetools import Scheme
from abjad.tools.schemetools import SchemePair


def test_schemetools_Scheme_01():
    r'''Scheme can be initialized from any value.
    '''

    scheme = Scheme(True)
    scheme = Scheme(False)
    scheme = Scheme(None)
    scheme = Scheme('hello')
    scheme = Scheme('hello world')
    scheme = Scheme((Scheme('foo'), Scheme(3.14159)))
    scheme = Scheme((SchemePair('padding', 1), SchemePair('attach-dir', -1)))


def test_schemetools_Scheme_02():
    r'''Scheme takes an optional `quoting` keyword, for prepending
    quote/unquote ticks.
    '''

    scheme = Scheme(('fus', 'ro', 'dah'), quoting = "',")
    assert str(scheme) == "',(fus ro dah)"


def test_schemetools_Scheme_03():
    r'''__str__ of Scheme returns the Scheme formatted value without the hash
    mark, while format(Scheme) returns the formatted value with the hash mark,
    allowing for nested Scheme expressions.
    '''

    scheme = Scheme(('fus', 'ro', 'dah'), quoting = "'")
    assert str(scheme) == "'(fus ro dah)"
    assert format(scheme) == "#'(fus ro dah)"


def test_schemetools_Scheme_04():
    r'''Scheme attempts to format Python values into Scheme equivalents.
    '''

    assert format(Scheme(True)) == '##t'
    assert format(Scheme(False)) == '##f'
    assert format(Scheme(None)) == '##f'
    assert format(Scheme('hello world')) == '#"hello world"'
    assert format(Scheme([1, 2, 3])) == '#(1 2 3)'
    assert format(Scheme((SchemePair('padding', 1), SchemePair('attach-dir', -1)), quoting="'")) == \
        "#'((padding . 1) (attach-dir . -1))"


def test_schemetools_Scheme_05():
    r'''Scheme wraps variable-length arguments into a tuple.
    '''

    assert format(Scheme(1, 2, 3)) == format(Scheme((1, 2, 3)))
