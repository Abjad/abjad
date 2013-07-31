# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Mark___setattr___01():
    r'''Slots constraint mark attributes.
    '''

    mark = marktools.Mark()

    assert py.test.raises(AttributeError, "mark.foo = 'bar'")
