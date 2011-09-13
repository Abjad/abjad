from abjad import *


def test_Measure_duration_is_underfull_01():

    t = Measure((3, 8), notetools.make_repeated_notes(3))
    assert not t.is_underfull

    contexttools.detach_time_signature_marks_attached_to_component(t)
    contexttools.TimeSignatureMark((4, 8))(t)
    assert t.is_underfull

    contexttools.detach_time_signature_marks_attached_to_component(t)
    contexttools.TimeSignatureMark((3, 8))(t)
    assert not t.is_underfull
