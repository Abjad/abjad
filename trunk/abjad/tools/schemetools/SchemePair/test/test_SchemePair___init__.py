from abjad import *


def test_SchemePair___init___01():
    '''Initialize Scheme pair from two values.
    '''

    scheme_pair = schemetools.SchemePair(1, 2)
    assert str(scheme_pair) == '(1 . 2)'

    scheme_pair = schemetools.SchemePair(True, False)
    assert str(scheme_pair) == '(#t . #f)'

    scheme_pair = schemetools.SchemePair('spacing', 4)
    assert str(scheme_pair) == '(spacing . 4)'


def test_SchemePair___init___02():
    '''Initialize Scheme pair from pair.
    '''

    scheme_pair = schemetools.SchemePair((1, 2))
    assert str(scheme_pair) == '(1 . 2)'


def test_SchemePair___init___03():
    '''Initialize Scheme pair from other Scheme pair.
    '''

    scheme_pair_1 = schemetools.SchemePair(1, 2)
    scheme_pair_2 = schemetools.SchemePair(scheme_pair_1)

    assert str(scheme_pair_1) == '(1 . 2)'
    assert str(scheme_pair_2) == '(1 . 2)'
    assert scheme_pair_1 is not scheme_pair_2
