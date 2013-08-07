# -*- encoding: utf-8 -*-
from abjad import *


def test_Measure_duration_is_underfull_01():

    measure = Measure((3, 8), notetools.make_repeated_notes(3))
    assert not measure.is_underfull

    measure.select().detach_marks(contexttools.TimeSignatureMark)
    contexttools.TimeSignatureMark((4, 8))(measure)
    assert measure.is_underfull

    measure.select().detach_marks(contexttools.TimeSignatureMark)
    contexttools.TimeSignatureMark((3, 8))(measure)
    assert not measure.is_underfull
