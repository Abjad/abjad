# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_resttools_Rest___setattr___01():
    r'''Slots constrain rest attributes.
    '''

    rest = Rest((1, 4))

    assert py.test.raises(AttributeError, "rest.foo = 'bar'")
