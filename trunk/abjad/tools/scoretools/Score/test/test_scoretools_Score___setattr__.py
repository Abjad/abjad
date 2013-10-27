# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_scoretools_Score___setattr___01():
    r'''Slots constrain score attributes.
    '''

    score = Score([])

    assert py.test.raises(AttributeError, "score.foo = 'bar'")
