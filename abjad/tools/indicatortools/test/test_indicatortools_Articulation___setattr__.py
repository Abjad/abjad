# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Articulation___setattr___01():
    r'''Slots constrain articulation attributes.
    '''

    articulation = Articulation('staccato')

    assert pytest.raises(AttributeError, "articulation.foo = 'bar'")
