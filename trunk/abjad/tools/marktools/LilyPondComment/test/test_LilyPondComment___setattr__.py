# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_LilyPondComment___setattr___01():
    r'''Slots constrain comment attributes.
    '''

    comment = marktools.LilyPondComment('foo')

    assert py.test.raises(AttributeError, "comment.foo = 'bar'")
