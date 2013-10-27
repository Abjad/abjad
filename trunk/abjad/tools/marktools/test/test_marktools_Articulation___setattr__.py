# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_marktools_Articulation___setattr___01():
    r'''Slots constrain articulation attributes.
    '''

    articulation = marktools.Articulation('staccato')

    assert py.test.raises(AttributeError, "articulation.foo = 'bar'")
