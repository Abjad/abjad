# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_indicatortools_Tempo_attach_01():

    score = Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    tempo = Tempo((1, 8), 52)
    attach(tempo, score[0][0])

    tempo = Tempo((1, 8), 52)
    assert pytest.raises(Exception, 'attach(tempo, score[0][0])')
    assert pytest.raises(Exception, 'attach(tempo, score[1][0])')
