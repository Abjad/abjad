# -*- encoding: utf-8 -*-
from abjad import *


def test_measuretools_Measure_duration_is_underfull_01():

    measure = Measure((3, 8), notetools.make_repeated_notes(3))
    assert not measure.is_underfull

    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    contexttools.TimeSignatureMark((4, 8))(measure)
    assert measure.is_underfull

    inspect(measure).get_mark(contexttools.TimeSignatureMark).detach()
    contexttools.TimeSignatureMark((3, 8))(measure)
    assert not measure.is_underfull
