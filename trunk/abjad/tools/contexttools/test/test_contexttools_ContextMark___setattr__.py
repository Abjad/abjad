# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_contexttools_ContextMark___setattr___01():
    r'''Slots constraint context mark attributes.
    '''

    context_mark = contexttools.ContextMark()

    assert py.test.raises(AttributeError, "context_mark.foo = 'bar'")
