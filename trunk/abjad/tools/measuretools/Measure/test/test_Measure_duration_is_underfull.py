from abjad import *


def test_Measure_duration_is_underfull_01():

    t = Measure((3, 8), notetools.make_repeated_notes(3))
    assert not t.is_underfull

    t.select().detach_marks(contexttools.TimeSignatureMark)
    contexttools.TimeSignatureMark((4, 8))(t)
    assert t.is_underfull

    t.select().detach_marks(contexttools.TimeSignatureMark)
    contexttools.TimeSignatureMark((3, 8))(t)
    assert not t.is_underfull
