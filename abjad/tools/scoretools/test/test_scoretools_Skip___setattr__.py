# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Skip___setattr___01():
    r'''Slots constrain skip attributes.
    '''

    skip = scoretools.Skip((1, 4))

    assert pytest.raises(AttributeError, "skip.foo = 'bar'")
