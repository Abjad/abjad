from abjad.tools.schemetools import Scheme
from abjad.tools.schemetools import SchemePair


def test_Scheme_01():
    '''Scheme can be initialized from any value.'''
    s = Scheme(True)
    s = Scheme(False)
    s = Scheme(None)
    s = Scheme('hello')
    s = Scheme('hello world')
    s = Scheme((Scheme('foo'), Scheme(3.14159)))
    s = Scheme((SchemePair('padding', 1), SchemePair('attach-dir', -1)))


def test_Scheme_02():
    '''Scheme takes an optional `quoting` keyword, for prepending quote/unquote ticks.'''
    s = Scheme(('fus', 'ro', 'dah'), quoting = "',")
    assert str(s) == "',(fus ro dah)"


def test_Scheme_03():
    '''__str__ of Scheme returns the Scheme formatted value without the hash mark,
    while Scheme.format returns the formatted value with the hash mark,
    allowing for nested Scheme expressions.'''
    s = Scheme(('fus', 'ro', 'dah'), quoting = "'")
    assert str(s) == "'(fus ro dah)"
    assert s.format == "#'(fus ro dah)"


def test_Scheme_04():
    '''Scheme attempts to format Python values into Scheme equivalents.'''
    assert Scheme(True).format == '##t'
    assert Scheme(False).format == '##f'
    assert Scheme(None).format == '##f'
    assert Scheme('hello world').format == '#"hello world"'
    assert Scheme([1, 2, 3]).format == '#(1 2 3)'
    assert Scheme((SchemePair('padding', 1), SchemePair('attach-dir', -1)), quoting="'").format == \
        "#'((padding . 1) (attach-dir . -1))"


def test_Scheme_05():
    '''Scheme wraps variable-length arguments into a tuple.'''
    assert Scheme(1, 2, 3).format == Scheme((1, 2, 3)).format
