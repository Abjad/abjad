# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_MetronomeMark_attach_01():

    score = Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    mark_1 = MetronomeMark((1, 8), 52)
    mark_2 = MetronomeMark((1, 8), 73)
    attach(mark_1, score[0][0])

    assert pytest.raises(Exception, 'attach(mark_2, score[1][0])')
