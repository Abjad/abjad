# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Measure___setattr___01():
    r'''Slots constraint measure attributes.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")

    assert pytest.raises(AttributeError, "measure.foo = 'bar'")
