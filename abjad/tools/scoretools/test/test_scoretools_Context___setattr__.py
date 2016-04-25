# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Context___setattr___01():
    r'''Slots constrain context attributes.
    '''

    context = scoretools.Context([])

    assert pytest.raises(AttributeError, "context.foo = 'bar'")
