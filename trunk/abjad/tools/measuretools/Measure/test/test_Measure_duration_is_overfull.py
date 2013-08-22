# -*- encoding: utf-8 -*-
from abjad import *


def test_Measure_duration_is_overfull_01():

    measure = Measure((3, 8), notetools.make_repeated_notes(3))
    assert not measure.is_overfull

    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    contexttools.TimeSignatureMark((2, 8))(measure)
    assert measure.is_overfull

    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    contexttools.TimeSignatureMark((3, 8))(measure)
    assert not measure.is_overfull
