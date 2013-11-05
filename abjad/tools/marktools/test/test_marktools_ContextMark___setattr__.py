# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_marktools_ContextMark___setattr___01():
    r'''Slots constraint context mark attributes.
    '''

    context_mark = marktools.ContextMark()

    assert pytest.raises(AttributeError, "context_mark.foo = 'bar'")
