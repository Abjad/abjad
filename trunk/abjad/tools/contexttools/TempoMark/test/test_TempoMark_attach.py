from abjad import *
import py


def test_TempoMark_attach_01():

    score = Score(r"\new Staff { c'' d'' e'' f'' } \new Staff { c' d' e' f' }")
    contexttools.TempoMark((1, 8), 52)(score[0][0])
    
    assert py.test.raises(ExtraMarkError, 'contexttools.TempoMark((1, 8), 52)(score[0][0])')
    assert py.test.raises(ExtraMarkError, 'contexttools.TempoMark((1, 8), 52)(score[1][0])')
