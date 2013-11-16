# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_indicatortools_Articulation___setattr___01():
    r'''Slots constrain articulation attributes.
    '''

    articulation = Articulation('staccato')

    assert pytest.raises(AttributeError, "articulation.foo = 'bar'")
