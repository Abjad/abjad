# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_duration_is_overfull_01():

    measure = Measure((3, 8), scoretools.make_repeated_notes(3))
    assert not measure.is_overfull

    inspect(measure).get_mark(marktools.TimeSignatureMark).detach()
    time_signature = marktools.TimeSignatureMark((2, 8))
    attach(time_signature, measure)
    assert measure.is_overfull

    inspect(measure).get_mark(marktools.TimeSignatureMark).detach()
    time_signature = marktools.TimeSignatureMark((3, 8))
    attach(time_signature, measure)
    assert not measure.is_overfull
