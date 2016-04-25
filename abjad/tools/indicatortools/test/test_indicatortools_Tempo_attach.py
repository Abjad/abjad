# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Tempo_attach_01():

    score = Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    tempo_1 = Tempo((1, 8), 52)
    tempo_2 = Tempo((1, 8), 73)
    attach(tempo_1, score[0][0])

    assert pytest.raises(Exception, 'attach(tempo_2, score[1][0])')
