# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_schemetools_SchemePair___setattr___01():
    r'''Scehem pairs are immutable.
    '''

    scheme_pair = schemetools.SchemePair('spacing', 4)
    assert py.test.raises(AttributeError, "scheme_pair.foo = 'bar'")
