# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Annotation___setattr___01():
    r'''Slots constrain annotation attributes.
    '''

    annotation = marktools.Annotation('foo')

    assert py.test.raises(AttributeError, "annotation.foo = 'bar'")
