# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.scoretools.Context import Context
import pytest


def test_scoretools_Context___setattr___01():
    r'''Slots constrain context attributes.
    '''

    context = Context([])

    assert pytest.raises(AttributeError, "context.foo = 'bar'")
