# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.scoretools.Context import Context
import py.test


def test_contexttools_Context___setattr___01():
    r'''Slots constrain context attributes.
    '''

    context = Context([])

    assert py.test.raises(AttributeError, "context.foo = 'bar'")
