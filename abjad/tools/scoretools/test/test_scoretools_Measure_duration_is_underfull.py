# -*- encoding: utf-8 -*-
from abjad import *


def test_scoretools_Measure_duration_is_underfull_01():

    measure = Measure((3, 8), scoretools.make_repeated_notes(3))
    assert not measure.is_underfull

    inspect(measure).get_mark(TimeSignatureMark).detach()
    time_signature = TimeSignatureMark((4, 8))
    attach(time_signature, measure)
    assert measure.is_underfull

    inspect(measure).get_mark(TimeSignatureMark).detach()
    time_signature = TimeSignatureMark((3, 8))
    attach(time_signature, measure)
    assert not measure.is_underfull
