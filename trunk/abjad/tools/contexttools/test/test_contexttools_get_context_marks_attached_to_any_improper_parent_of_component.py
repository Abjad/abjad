from abjad import *


def test_contexttools_get_context_marks_attached_to_any_improper_parent_of_component_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    clef = contexttools.ClefMark('treble')(staff)
    dynamic = contexttools.DynamicMark('f')(staff[0])

    context_marks = contexttools.get_context_marks_attached_to_any_improper_parent_of_component(staff[0])

    assert len(context_marks) == 2
    assert clef in context_marks
    assert dynamic in context_marks
