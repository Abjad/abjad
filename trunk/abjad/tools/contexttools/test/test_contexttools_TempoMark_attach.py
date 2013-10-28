# -*- encoding: utf-8 -*-
import py
from abjad import *


def test_contexttools_TempoMark_attach_01():

    score = Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    tempo = contexttools.TempoMark((1, 8), 52)
    tempo.attach(score[0][0])

    tempo = contexttools.TempoMark((1, 8), 52)
    assert py.test.raises(ExtraMarkError, 'tempo.attach(score[0][0])')
    assert py.test.raises(ExtraMarkError, 'tempo.attach(score[1][0])')
