# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_duration_is_overfull_01():

    measure = Measure((3, 8), "c'8 c'8 c'8")
    assert not measure.is_overfull

    detach(TimeSignature, measure)
    time_signature = TimeSignature((2, 8))
    attach(time_signature, measure)
    assert measure.is_overfull

    detach(TimeSignature, measure)
    time_signature = TimeSignature((3, 8))
    attach(time_signature, measure)
    assert not measure.is_overfull
