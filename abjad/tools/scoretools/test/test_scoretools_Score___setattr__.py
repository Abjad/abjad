# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Score___setattr___01():
    r'''Slots constrain score attributes.
    '''

    score = Score([])

    assert pytest.raises(AttributeError, "score.foo = 'bar'")
