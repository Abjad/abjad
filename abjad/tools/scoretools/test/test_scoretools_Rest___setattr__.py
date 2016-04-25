# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Rest___setattr___01():
    r'''Slots constrain rest attributes.
    '''

    rest = Rest((1, 4))

    assert pytest.raises(AttributeError, "rest.foo = 'bar'")
