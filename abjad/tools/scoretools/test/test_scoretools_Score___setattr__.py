# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Score___setattr___01():
    r'''Slots constrain score attributes.
    '''

    score = Score([])

    assert pytest.raises(AttributeError, "score.foo = 'bar'")
