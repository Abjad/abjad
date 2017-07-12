# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Measure_duration_is_underfull_01():

    measure = abjad.Measure((3, 8), "c'8 c'8 c'8")
    assert not measure.is_underfull

    abjad.detach(abjad.TimeSignature, measure)
    time_signature = abjad.TimeSignature((4, 8))
    abjad.attach(time_signature, measure)
    assert measure.is_underfull

    abjad.detach(abjad.TimeSignature, measure)
    time_signature = abjad.TimeSignature((3, 8))
    abjad.attach(time_signature, measure)
    assert not measure.is_underfull
