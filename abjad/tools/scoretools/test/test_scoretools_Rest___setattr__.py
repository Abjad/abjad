# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Rest___setattr___01():
    r'''Slots constrain rest attributes.
    '''

    rest = Rest((1, 4))

    assert pytest.raises(AttributeError, "rest.foo = 'bar'")
