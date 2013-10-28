# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_Measure_duration_is_overfull_01():

    measure = Measure((3, 8), notetools.make_repeated_notes(3))
    assert not measure.is_overfull

    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    time_signature = contexttools.TimeSignatureMark((2, 8))
    attach(time_signature, measure)
    assert measure.is_overfull

    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    time_signature = contexttools.TimeSignatureMark((3, 8))
    attach(time_signature, measure)
    assert not measure.is_overfull
